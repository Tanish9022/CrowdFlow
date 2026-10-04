import os

docs_dir = "docs"

docs = {}

docs["11_MODEL_TRAINING_PLAN.md"] = r"""# 11. Model Training Plan

## 1. Objectives & Hardware Budget
- **Target Platform:** Intel Core i3 (Quad-Core), 8 GB RAM, CPU-only execution (or optional Google Colab T4 GPU instance for fast fine-tuning).
- **Primary Model:** YOLOv8 Nano (`yolov8n.pt`) with transfer learning from MS COCO weights.
- **Secondary Model:** Feature-based tabular classifier (Random Forest / XGBoost) for traffic state verification where rule thresholds require validation.

## 2. Object Detector Fine-Tuning Specification

### Hyperparameter Configurations
| Parameter | Value | Justification |
| :--- | :--- | :--- |
| **Base Model** | `yolov8n.pt` | Smallest footprint (3.2M params), fastest inference on CPU. |
| **Image Resolution (`imgsz`)** | 640 | Balances small two-wheeler resolution with CPU throughput. |
| **Batch Size** | 16 (GPU) / 4 (CPU) | Fits comfortably in 8 GB RAM without thrashing swap space. |
| **Epochs** | 50 | Early stopping at patience=10 prevents overfitting on small datasets. |
| **Optimizer** | AdamW | Fast convergence with weight decay ($1 \times 10^{-4}$). |
| **Initial Learning Rate ($\eta_0$)** | $0.001$ | Standard transfer learning rate with cosine annealing decay. |
| **Augmentation** | Mosaic ($0.5$), Fliplr ($0.5$), HSV ($h=0.015, s=0.7, v=0.4$) | Enhances resilience to changing sunlight, shadows, and occlusions. |

### Evaluation Metrics
- $\text{mAP}@0.5$ (Mean Average Precision at IoU 0.5)
- $\text{mAP}@0.5:0.95$ (Stricter COCO evaluation)
- Precision, Recall, and per-class F1-score for: `car`, `motorcycle`, `bus`, `truck`, `person`.

## 3. Traffic State Classifier Training (Random Forest)

### Feature Vector Input
$$\vec{x} = [N_{\text{veh}}, \bar{v}_{\text{kmh}}, \Delta v, \rho_{\text{occ}}, r_{\text{stat}}, L_{\text{queue}}, t_{\text{persist}}, N_{\text{ped}}, S_{\text{signal}}]$$
Where:
- $N_{\text{veh}}$: Total detected vehicles within road ROI
- $\bar{v}_{\text{kmh}}$: Average velocity in km/h
- $\Delta v$: Velocity variance
- $\rho_{\text{occ}}$: Bounding-box area over drivable road ROI area
- $r_{\text{stat}}$: Ratio of stationary vehicles ($\le 3 \text{ km/h}$) to total vehicles
- $L_{\text{queue}}$: Estimated queue length in meters
- $t_{\text{persist}}$: Continuous time queue has persisted (seconds)
- $N_{\text{ped}}$: Pedestrians detected on road surface
- $S_{\text{signal}}$: Signal state ($0 = \text{Green}, 1 = \text{Red}, -1 = \text{Unknown/Uncontrolled}$)

### Classifier Parameters
- Model: `RandomForestClassifier(n_estimators=100, max_depth=6, class_weight='balanced')`
- Validation Strategy: Stratified 5-Fold Cross Validation grouped by Video ID.
- Baseline Accuracy Target: $\ge 88\%$ cross-validation macro F1-score across 7 traffic states.
"""

docs["12_VEHICLE_TRACKING.md"] = r"""# 12. Vehicle Tracking

## 1. Tracking Objectives
Vehicle detection alone cannot measure speed, stationary duration, or direction of travel. Multi-object tracking (MOT) associates bounding boxes across successive video frames, producing temporal trajectories (tracklets) identified by unique integer IDs.

## 2. Tracking Architecture: ByteTrack & Centroid Kalman Association

```mermaid
graph TD
    DETS[Frame Detections from YOLO] --> SPLIT{Confidence Score}
    SPLIT -- "Conf >= 0.5 (High)" --> DET_HIGH[High Confidence Detections]
    SPLIT -- "0.1 <= Conf < 0.5 (Low)" --> DET_LOW[Low Confidence Detections]
    
    PRED[Kalman Filter Track State Prediction] --> MATCH1[First Association: High Conf Detections with Tracks]
    DET_HIGH --> MATCH1
    MATCH1 -- "Matched" --> UPDATE1[Update Track States]
    MATCH1 -- "Unmatched Tracks" --> MATCH2[Second Association: Low Conf Detections with Remaining Tracks]
    DET_LOW --> MATCH2
    MATCH2 -- "Matched" --> UPDATE2[Recover Occluded Tracks]
    MATCH2 -- "Still Unmatched" --> LOST[Mark Track as Lost / Expired]
```

## 3. Tracking Algorithm Specifications

### 3.1 State Vector Representation
For each vehicle $i$, the Kalman filter maintains an 8-dimensional state vector:
$$\mathbf{x} = [x_c, y_c, a, h, \dot{x}_c, \dot{y}_c, \dot{a}, \dot{h}]^T$$
Where $(x_c, y_c)$ is the bounding box center, $a = w/h$ is the aspect ratio, $h$ is height, and their respective time derivatives represent velocities.

### 3.2 Association Metric
- Primary: Intersection over Union (IoU) between predicted Kalman bounding box and detected bounding box.
- Cost matrix solved using the Hungarian algorithm (`scipy.optimize.linear_sum_assignment`).
- Distance threshold: $\text{IoU}_{\text{threshold}} = 0.3$.

### 3.3 Trajectory History & Speed Estimation
- Rolling FIFO window of up to 30 frame centroids: $\mathcal{T}_i = \{(x_t, y_t, \tau_t)\}_{t=0}^k$.
- Pixel displacement $\Delta d_{\text{px}} = \sqrt{(x_k - x_0)^2 + (y_k - y_0)^2}$.
- Calibrated metric displacement: $\Delta d_{\text{meters}} = \Delta d_{\text{px}} \times s_{\text{scale}}$ where $s_{\text{scale}}$ is derived from camera calibration.
- Instantaneous Speed:
  $$v_i = \left(\frac{\Delta d_{\text{meters}}}{\Delta t}\right) \times 3.6 \quad [\text{km/h}]$$
- Stationary Classification: If $v_i < 3.0 \text{ km/h}$ for $\Delta t > 3.0 \text{ seconds}$, vehicle $i$ is flagged as `IS_STATIONARY`.
"""

docs["13_TRAFFIC_STATE_ENGINE.md"] = r"""# 13. Traffic State Engine

## 1. Architectural Distinction: Detection vs. Traffic State
> [!IMPORTANT]
> **Fundamental Principle:** Vehicle detection $\neq$ Traffic detection.
> A frame containing 40 stationary vehicles is not automatically a traffic jam—it could be a normal red light queue waiting for a green signal, or vehicles lawfully parked on a road shoulder. The Traffic State Engine interprets extracted kinematic and spatial features over time to deduce systemic road condition.

## 2. Traffic State Enumeration

| State Name | Color Code | Description | Typical Real-World Scenario |
| :--- | :--- | :--- | :--- |
| `FREE_FLOW` | Green | High average speed, low road density, minimal stops. | Late-night arterial, open highway. |
| `NORMAL` | Emerald | Moderate steady speed, safe inter-vehicle headway. | Standard midday traffic conditions. |
| `SLOW` | Amber | Speed significantly below posted limit, dense platoon. | Heavy peak hour, narrow road bottleneck. |
| `SIGNAL_QUEUE` | Yellow | Vehicles stationary at intersection while signal is RED, moving promptly once GREEN. | Normal cyclic junction pause. |
| `TRAFFIC_QUEUE` | Orange | Vehicle line extending beyond intersection spillover, persisting across green phases. | Inadequate green cycle, minor bottleneck. |
| `HEAVY_CONGESTION`| Red | Average speed $< 5\text{ km/h}$, density $>80\%$, stationary ratio $>70\%$ without signal justification. | Severe gridlock, downstream blockage. |
| `PARKED` | Gray | Vehicles stationary $>300\text{ s}$ outside primary travel lanes (shoulders/bays). | On-street parking, taxi stands. |
| `PEDESTRIAN_CROWD`| Purple | High density of pedestrian detections on carriageway; vehicular flow halted or diverted. | Protest rally, religious procession, fair. |

## 3. Road Operability Mapping
From the granular traffic states, the higher-level Road Operability is derived for graph routing:
- **`OPEN`**: States `FREE_FLOW`, `NORMAL`.
- **`SLOW`**: States `SLOW`, `SIGNAL_QUEUE`.
- **`CONGESTED`**: States `TRAFFIC_QUEUE`, `HEAVY_CONGESTION`.
- **`PARTIALLY_BLOCKED`**: State `PARKED` obstructing travel lanes, or low-density road work.
- **`BLOCKED`**: State `PEDESTRIAN_CROWD` (unplanned protest) or zero throughput with infinite queue persistence ($t_{\text{persist}} > 180\text{ s}$ and $\bar{v} \approx 0$).
"""

docs["14_QUEUE_AND_CONGESTION_DETECTION.md"] = r"""# 14. Queue and Congestion Detection

## 1. Feature Formulations

### 1.1 Road Area Occupancy Ratio ($\rho_{\text{occ}}$)
Let $\mathcal{A}_{\text{ROI}}$ be the pixel area of the defined drivable road polygon. For $N$ detected vehicles inside the polygon with bounding box areas $a_i = w_i \times h_i$:
$$\rho_{\text{occ}} = \min\left(1.0, \, \frac{\sum_{i=1}^N (a_i \cap \mathcal{A}_{\text{ROI}})}{\mathcal{A}_{\text{ROI}}}\right)$$

### 1.2 Stationary Fraction ($r_{\text{stat}}$)
Let $N_{\text{stat}}$ be the count of vehicles tracked inside the ROI with speed $v_i \le v_{\text{threshold}}$ ($3 \text{ km/h}$):
$$r_{\text{stat}} = \frac{N_{\text{stat}}}{\max(1, N_{\text{total}})}$$

### 1.3 Queue Persistence Duration ($t_{\text{persist}}$)
Queue persistence measures the unbroken time window (in seconds) during which $r_{\text{stat}} \ge 0.60$ and $N_{\text{total}} \ge N_{\text{min\_queue}}$:
$$t_{\text{persist}} = t_{\text{current}} - t_{\text{queue\_start}}$$
If the queue dissipates for more than 5 consecutive seconds, $t_{\text{persist}}$ resets to zero.

## 2. Decision Logic Tree

```mermaid
flowchart TD
    START[Frame Features Ingested] --> PED{Pedestrian Ratio > 0.40 & Count > 15?}
    PED -- Yes --> S_CROWD[State = PEDESTRIAN_CROWD]
    PED -- No --> OCC{Occupancy Ratio > 0.30?}
    OCC -- No --> S_FREE[State = FREE_FLOW]
    OCC -- Yes --> SPD{Average Speed < 8 km/h & Stationary Ratio > 0.50?}
    SPD -- No --> S_NORM[State = NORMAL / SLOW]
    SPD -- Yes --> SIG{Signal Data Available?}
    SIG -- Yes & Signal is RED --> RED_TIME{Queue Time < Signal Red Duration + 10s?}
    RED_TIME -- Yes --> S_SIGQ[State = SIGNAL_QUEUE]
    RED_TIME -- No --> S_TRAFQ[State = TRAFFIC_QUEUE / CONGESTED]
    SIG -- No or Green --> PERSIST{Queue Persistence > 120s?}
    PERSIST -- Yes --> S_HEAVY[State = HEAVY_CONGESTION / BLOCKED]
    PERSIST -- No --> S_TRAFQ
```

## 3. Explaining Queue vs. Congestion in Viva
1. **Signal Queue:** Cyclic, expected, self-clearing when green light appears. The queue length decreases from front to back during the green phase.
2. **Traffic Congestion Queue:** Persistent, non-clearing across multiple cycles; tail of the queue grows faster than head can discharge.
3. **Parked Non-Traffic:** Spatial clustering on curbside ROI without vehicle headways changing over several minutes.
"""

docs["15_ROAD_GRAPH_JIGSAW_ENGINE.md"] = r"""# 15. Road Graph Jigsaw Engine

## 1. Graph Theoretical Representation
The urban road network is modeled as a weighted directed multigraph $G = (V, E)$:
- **Vertices ($V$):** Physical road intersections and major decision junctions:
  $$V = \{v_1, v_2, \dots, v_n\}$$
  Each vertex possesses geographical or grid coordinates: $v_i = (\text{id}, \text{name}, x, y, \text{type})$.
- **Directed Edges ($E$):** Drivable road segments connecting junctions:
  $$e_k = (u, v, k) \in E \quad \text{where } u, v \in V$$
  Edge attributes include:
  $$\text{attr}(e_k) = \{\text{road\_id}, \text{length\_m}, \text{lanes}, \text{capacity\_vph}, v_{\text{free}}, \rho(t), \bar{v}(t), \text{status}\}$$

## 2. The Jigsaw Puzzle Metaphor in Graph Theory
In a classic jigsaw puzzle, every interlocking piece must fit to maintain structural continuity. In urban traffic:
1. Each road segment $e_k$ is an active "puzzle piece" carrying dynamic vehicle flow $q(e_k)$.
2. When an edge is declared `BLOCKED` (e.g., due to an accident or protest on $e_{\text{blocked}}$), that piece is conceptually **removed from the puzzle**.
3. Removing $e_{\text{blocked}}$ creates an impedance void: the cost of traversing $e_{\text{blocked}}$ becomes:
   $$W(e_{\text{blocked}}) = \infty$$
4. The volume $q(e_{\text{blocked}})$ formerly carried by the disabled link cannot vanish; it must be assembled into neighboring puzzle pieces (parallel corridors) without exceeding their structural capacities.

```
       [Junction 1] ───(Road R1: Open)───► [Junction 2]
            │                                   │
      (Road R4: Open)                    (Road R2: Heavy)
            │                                   ▼
            ▼                            [Junction 4]
       [Junction 3] ───[Road R3: BLOCKED]───► (Missing Piece)
                         (Detour diverted via R4 & R5)
```

## 3. Dynamic Edge Weight (Cost) Formula
Crowd Flow does not route purely on physical distance $d(e)$. Edge cost represents **Generalized Impedance** incorporating delay, congestion, and capacity saturation:

$$W(e) = d(e) \cdot \left[ 1 + \alpha \cdot \left(\frac{q(e)}{C(e)}\right)^\beta \right] \cdot \left( \frac{v_{\text{free}}(e)}{\max(v_{\text{min}}, \bar{v}(e))} \right) + \Omega(e)$$

Where:
- $d(e)$: Physical road length in meters.
- $q(e)$: Observed or estimated vehicle volume (vehicles/hour).
- $C(e)$: Practical capacity of the road segment (vehicles/hour).
- $\alpha, \beta$: Standard BPR (Bureau of Public Roads) calibration coefficients (default: $\alpha = 0.15, \beta = 4.0$).
- $v_{\text{free}}(e)$: Design free-flow speed (e.g., $50\text{ km/h}$).
- $\bar{v}(e)$: Current real-time average speed measured via CCTV.
- $v_{\text{min}}$: Speed lower-bound threshold ($2.0\text{ km/h}$) to prevent division by zero.
- $\Omega(e)$: Penalty term:
  $$\Omega(e) = \begin{cases} 0 & \text{if status is OPEN} \\ 500 & \text{if status is SLOW} \\ 2000 & \text{if status is CONGESTED} \\ \infty & \text{if status is BLOCKED} \end{cases}$$
"""

docs["16_ROUTE_OPTIMIZATION.md"] = r"""# 16. Route Optimization

## 1. Routing Engine Architecture
The Route Optimization engine computes optimal paths between any source junction $s \in V$ and destination junction $t \in V$ using dynamic link costs supplied by the Jigsaw Engine.

## 2. Modified Dijkstra Algorithm with Dynamic Impedance

```python
import heapq

def dijkstra_dynamic(graph, start_node, target_node):
    # Priority queue stores tuples of (current_cost, current_node, path_taken)
    pq = [(0.0, start_node, [start_node])]
    visited_costs = {node: float('inf') for node in graph.nodes}
    visited_costs[start_node] = 0.0

    while pq:
        current_cost, u, path = heapq.heappop(pq)

        if u == target_node:
            return {
                "found": True,
                "cost": current_cost,
                "path": path,
                "distance_meters": calculate_path_distance(graph, path)
            }

        if current_cost > visited_costs[u]:
            continue

        for v in graph.neighbors(u):
            edge = graph.get_edge_data(u, v)
            # If road is physically blocked, edge cost is effectively infinite
            if edge.get("status") == "BLOCKED" or edge.get("cost") >= float('inf'):
                continue

            edge_weight = edge.get("dynamic_cost", edge.get("distance_m", 100))
            new_cost = current_cost + edge_weight

            if new_cost < visited_costs[v]:
                visited_costs[v] = new_cost
                heapq.heappush(pq, (new_cost, v, path + [v]))

    return {"found": False, "cost": float('inf'), "path": [], "message": "No feasible detour route found."}
```

## 3. Alternative Multi-Path Detour Generation (K-Shortest Paths)
To prevent creating a secondary bottleneck by dumping 100% of diverted traffic onto a single alternative street, the system computes **$K$ Loopless Alternative Paths** ($K=3$) using Yen's algorithm:
- **Path 1 (Primary Detour):** Minimum impedance alternative route.
- **Path 2 (Secondary Detour):** Next best corridor utilizing an adjacent parallel arterial.
- **Path 3 (Tertiary Detour):** Outer ring bypass route for heavy multi-axle vehicles/buses.

The operator dashboard displays all $K$ alternatives with relative travel time estimations and capacity headrooms.
"""

docs["17_TRAFFIC_SIMULATION.md"] = r"""# 17. Traffic Simulation

## 1. Macroscopic What-If Simulation Model
Crowd Flow implements a transparent, controlled macroscopic traffic redistribution model. It simulates the systemic redistribution of vehicle flow across the network when one or more road links are severed or throttled.

## 2. Mathematical Redistribution Formulation
Let road link $e_b \in E$ be marked `BLOCKED`.
Let $Q_{\text{displaced}} = q(e_b)$ be the vehicular volume (vehicles/hour) that previously utilized $e_b$.

### Capacity-Elasticity Weight Allocation
The diverted traffic is distributed across $M$ candidate alternative detour paths $\{P_1, P_2, \dots, P_M\}$ connecting the upstream diversion point to downstream convergence junctions.

The proportion of flow $\gamma_m$ assigned to alternative path $P_m$ is governed by a Logit discrete-choice model based on available residual capacity $C_{\text{res}}(P_m)$ and path impedance $W(P_m)$:
$$\gamma_m = \frac{\exp(-\theta \cdot W(P_m)) \cdot C_{\text{res}}(P_m)}{\sum_{j=1}^M \exp(-\theta \cdot W(P_j)) \cdot C_{\text{res}}(P_j)}$$
Where $\theta$ is the route sensitivity dispersion parameter (default: $\theta = 0.005$).

### Projected Volume & Occupancy Calculation
For each edge $e$ participating in detour path $P_m$:
$$q_{\text{simulated}}(e) = q_{\text{baseline}}(e) + \sum_{m: e \in P_m} \gamma_m \cdot Q_{\text{displaced}}$$
The simulated occupancy ratio is:
$$\rho_{\text{simulated}}(e) = \min\left(1.0, \, \rho_{\text{baseline}}(e) + \frac{\Delta q(e)}{C(e)}\right)$$

## 3. Before vs. After Simulation Telemetry Output
When an operator executes a simulation, the service produces a comparative delta:
```json
{
  "scenario_id": "SIM_PROTEST_JM_01",
  "blocked_road": "R_JM_NORTH",
  "displaced_volume_vph": 1250,
  "summary": {
    "total_affected_roads": 4,
    "overloaded_roads_count": 1,
    "average_network_delay_increase_percent": 24.8
  },
  "edges_comparison": [
    {
      "road_id": "R_FC_ROAD",
      "baseline_occupancy": 0.55,
      "simulated_occupancy": 0.88,
      "status_before": "NORMAL",
      "status_after": "CONGESTED",
      "is_overloaded": true
    },
    {
      "road_id": "R_SENAPATI_BAPAT",
      "baseline_occupancy": 0.32,
      "simulated_occupancy": 0.49,
      "status_before": "OPEN",
      "status_after": "OPEN",
      "is_overloaded": false
    }
  ]
}
```
"""

docs["18_SIGNAL_RECOMMENDATION.md"] = r"""# 18. Signal Recommendation

## 1. Advisory Signal Rebalancing Logic
When a road is blocked and traffic is diverted onto an alternative corridor, intersections along that detour path experience an abnormal surge in volume on one specific approach arm. Static fixed-time signal plans cause extreme queue backups on that arm.

Crowd Flow calculates an **Advisory Signal Timing Plan** to dynamically reallocate green phase time toward the overloaded detour approach.

> [!CAUTION]
> **Safety & Real-World Mandate:** The academic system produces **Advisories for Human Operator Approval**. It does not directly actuate roadside signal hardware.

## 2. Green Split Reallocation (Webster-Equisaturation Formulation)
Consider a 4-leg junction with Cycle Time $C_{\text{cycle}}$ (e.g., 90 seconds) and Lost Time $L = 8\text{ seconds}$ (yellow + all-red clearance intervals).
Total effective green time available:
$$G_{\text{total}} = C_{\text{cycle}} - L$$

Let $q_1, q_2, \dots, q_k$ be the observed or simulated critical lane volumes for the competing signal phases (e.g., Phase 1 = North-South Arterial, Phase 2 = East-West Cross Street), with saturation flows $S_1, S_2, \dots, S_k$.

The flow ratio for phase $i$ is:
$$y_i = \frac{q_i}{S_i}, \quad Y = \sum_{i=1}^k y_i$$

The recommended green phase time $g_i$ is distributed in proportion to flow ratios:
$$g_i = \left(\frac{y_i}{Y}\right) \times G_{\text{total}}$$

Subject to boundary constraints:
$$g_{\text{min}} \le g_i \le g_{\text{max}}$$
(e.g., $g_{\text{min}} = 15\text{ s}$ for pedestrian clearance, $g_{\text{max}} = 70\text{ s}$ to prevent cross-street starvation).

## 3. Example Advisory Output
```
Junction: J04 (Swargate Chowk)
Current Signal Cycle: 90s
  - Approach North-South (Detour Path): Green = 35s | Red = 55s
  - Approach East-West:                 Green = 45s | Red = 45s

Observed Disruption: Road R02 Blocked; Diverted flow +650 vph onto North-South approach.
Calculated Demand Ratio: North-South = 0.65 | East-West = 0.35

RECOMMENDED ADVISORY PLAN:
  - Approach North-South: Green = 55s (+20s) | Red = 35s
  - Approach East-West:   Green = 27s (-18s) | Red = 63s

Expected Impact: Prevents detour queue spillback by 42%; estimated average vehicle delay reduction = 18.5 seconds/veh.
```
"""

docs["19_DATABASE_DESIGN.md"] = r"""# 19. Database Design

## 1. Relational Schema Architecture
The Crowd Flow database stores user credentials, road network topology, camera calibration mappings, time-series telemetry observations, alert records, and simulation runs.

## 2. Entity Relationship (ER) Diagram

```mermaid
erDiagram
    USERS ||--o{ AUDIT_LOGS : generates
    CAMERAS ||--o{ ROAD_EDGES : monitors
    CAMERAS ||--o{ TRAFFIC_OBSERVATIONS : records
    ROAD_NODES ||--o{ ROAD_EDGES : "source / destination"
    ROAD_EDGES ||--o{ TRAFFIC_OBSERVATIONS : measures
    ROAD_EDGES ||--o{ ALERTS : triggers
    ROAD_NODES ||--o{ TRAFFIC_SIGNALS : contains
    TRAFFIC_SIGNALS ||--o{ SIGNAL_RECOMMENDATIONS : receives
    SIMULATIONS ||--o{ SIMULATION_RESULTS : produces

    USERS {
        int id PK
        string username UK
        string hashed_password
        string role
        string full_name
        datetime created_at
    }

    ROAD_NODES {
        int id PK
        string node_id UK
        string name
        float latitude
        float longitude
        string node_type
    }

    ROAD_EDGES {
        int id PK
        string road_id UK
        string name
        int source_node_id FK
        int target_node_id FK
        float length_meters
        int lanes
        int capacity_vph
        float free_flow_speed
        string current_status
        float current_occupancy
    }

    CAMERAS {
        int id PK
        string camera_id UK
        string name
        string stream_url
        int monitored_road_id FK
        string status
        json roi_polygon
        float fps
    }

    TRAFFIC_OBSERVATIONS {
        int id PK
        int camera_id FK
        int road_id FK
        datetime recorded_at
        int vehicle_count
        int pedestrian_count
        float average_speed_kmh
        float occupancy_ratio
        int stationary_count
        float queue_length_m
        string traffic_state
    }

    ALERTS {
        int id PK
        int road_id FK
        string alert_type
        string severity
        string message
        datetime triggered_at
        boolean is_acknowledged
    }

    TRAFFIC_SIGNALS {
        int id PK
        int node_id FK
        string junction_name
        int cycle_time_s
        json phase_timings
    }

    SIGNAL_RECOMMENDATIONS {
        int id PK
        int signal_id FK
        datetime recommended_at
        json current_timings
        json recommended_timings
        string justification
        boolean accepted_by_operator
    }
```

## 3. Database Indexes for Performance
- `idx_obs_road_time`: Composite index on `TRAFFIC_OBSERVATIONS(road_id, recorded_at DESC)` for fast dashboard graph queries.
- `idx_alerts_active`: Index on `ALERTS(is_acknowledged, triggered_at DESC)` for real-time notification feeds.
- `idx_road_status`: Index on `ROAD_EDGES(current_status)` for instant graph impedance compilation.
"""

docs["20_API_SPECIFICATION.md"] = r"""# 20. API Specification

## 1. RESTful API Architecture
The backend exposes high-performance asynchronous REST endpoints along with WebSocket streams for live dashboard push telemetry. All endpoints return standard JSON responses with HTTP status codes.

## 2. Core API Endpoints

### 2.1 Authentication & System
- `POST /api/v1/auth/login`: Form-encoded credentials (`username`, `password`), returns JWT Bearer token.
- `GET /api/v1/auth/me`: Current authenticated user profile and roles.
- `GET /api/v1/health`: System health, uptime, and database connection status.

### 2.2 Network Topology & Jigsaw Graph
- `GET /api/v1/network/graph`: Full network topology (nodes, directed edges, current statuses, coordinates, dynamic costs).
- `GET /api/v1/network/roads/{road_id}`: Granular live details and time-series for a single road link.
- `PATCH /api/v1/network/roads/{road_id}/status`: Manual operator override of road status (`OPEN`, `SLOW`, `CONGESTED`, `BLOCKED`).

### 2.3 Camera Surveillance & AI Stream
- `GET /api/v1/cameras`: List all registered CCTV camera sources and their monitoring statuses.
- `GET /api/v1/cameras/{camera_id}/telemetry`: Latest observation snapshot (counts, speed, state, queue length).
- `GET /api/v1/cameras/{camera_id}/feed`: MJPEG stream endpoint for web dashboard rendering with AI bounding box overlays.

### 2.4 Routing & Navigation
- `POST /api/v1/routing/calculate`:
  - Request: `{"source_node": "J01", "destination_node": "J08", "avoid_blocked": true}`
  - Response: `{"primary_route": [...], "distance_m": 1420, "estimated_time_s": 185, "alternatives": [...]}`

### 2.5 What-If Jigsaw Simulation
- `POST /api/v1/simulation/run`:
  - Request: `{"blocked_road_id": "ROAD_03", "disruption_type": "PROTEST", "diverted_volume_vph": 1100}`
  - Response: Full simulation delta with before/after occupancies, overloaded links, and redistribution percentages.

### 2.6 Signal Advisory
- `GET /api/v1/signals/recommendations`: Active signal timing recommendations for all network junctions.
- `POST /api/v1/signals/{signal_id}/acknowledge`: Mark recommendation as reviewed/implemented by operator.

### 2.7 WebSocket Real-Time Telemetry
- `WS /api/v1/ws/telemetry`: Continuous broadcast of network metrics, active alerts, and camera FPS updates at $1\text{ Hz}$.
"""

for fname, content in docs.items():
    with open(os.path.join(docs_dir, fname), "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

print(f"Generated {len(docs)} documents successfully (Part 2).")
