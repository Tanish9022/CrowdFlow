import os

docs_dir = "docs"

docs = {}

docs["21_BACKEND_IMPLEMENTATION.md"] = r"""# 21. Backend Implementation

## 1. Backend Architecture & Package Structure
The backend is structured as a modular FastAPI enterprise application following Domain-Driven Design (DDD) principles:

```
backend/
├── app/
│   ├── main.py              # Application entrypoint & lifespan hooks
│   ├── core/
│   │   ├── config.py        # Settings management via pydantic-settings (.env)
│   │   ├── security.py      # JWT creation, bcrypt password hashing
│   │   └── events.py        # Startup/shutdown hooks
│   ├── database/
│   │   ├── session.py       # SQLAlchemy engine & sessionmaker
│   │   └── base.py          # Declarative Base metadata
│   ├── models/              # SQLAlchemy ORM models (User, Road, Camera, etc.)
│   ├── schemas/             # Pydantic v2 validation models for DTOs
│   ├── api/                 # Versioned REST routers (/v1/network, /v1/cameras, etc.)
│   ├── services/            # Business orchestration services
│   ├── cv/                  # Video ingestion, YOLOv8 detector, ROI polygon tester
│   ├── tracking/            # Multi-object tracking (ByteTrack / Centroid Kalman)
│   ├── traffic/             # Feature aggregation, rule & RF state engine
│   ├── graph/               # NetworkX graph manager, dynamic cost calculation
│   ├── routing/             # Modified Dijkstra & alternative detour solver
│   ├── simulation/          # Macroscopic What-If redistribution engine
│   ├── recommendations/     # Webster advisory signal split engine
│   └── utils/               # Coordinate math, logging helpers, formatting
```

## 2. Concurrency & Async Processing Model
- **Web Requests:** Handled asynchronously via `async def` endpoints on the Uvicorn ASGI event loop.
- **Computer Vision Inference:** Video decoding and YOLO tensor calculations run in dedicated background worker threads or sub-processes (`asyncio.to_thread` / `concurrent.futures.ThreadPoolExecutor`) to prevent blocking API request handling.
- **In-Memory Cache:** Current dynamic graph weights and active camera states are cached in thread-safe in-memory singletons, with asynchronous periodic persistence to the relational database.
"""

docs["22_FRONTEND_IMPLEMENTATION.md"] = r"""# 22. Frontend Implementation

## 1. Frontend Architecture & Directory Layout
The frontend is built using React 18 with a clean component-based layout:

```
frontend/
├── src/
│   ├── main.jsx             # React entrypoint
│   ├── App.jsx              # App root & route definitions
│   ├── index.css            # Obsidian design tokens & global styles
│   ├── layouts/
│   │   ├── MainLayout.jsx   # Topbar, sidebar navigation, alert drawer
│   │   └── AuthLayout.jsx   # Minimal authentication shell
│   ├── pages/
│   │   ├── Dashboard.jsx    # Main operations dashboard
│   │   ├── Monitoring.jsx   # Multi-CCTV video grid with overlays
│   │   ├── JigsawMap.jsx    # Signature interactive vector road network
│   │   ├── Simulator.jsx    # What-If redistribution comparison view
│   │   ├── Routing.jsx      # Detour and alternative path planner
│   │   ├── Signals.jsx      # Advisory signal timing screen
│   │   ├── Analytics.jsx    # Time-series graphs & heatmaps
│   │   └── Settings.jsx     # Thresholds, ROI calibration & camera config
│   ├── components/
│   │   ├── common/          # Buttons, Modal, Badge, Tooltip, Card
│   │   ├── video/           # MJPEG / Video player canvas with detection overlays
│   │   ├── graph/           # SVG-based dynamic Jigsaw road network
│   │   └── telemetry/       # Live KPI cards, sparklines, queue indicators
│   ├── hooks/
│   │   ├── useTelemetry.js  # WebSocket subscription to live updates
│   │   └── useRoadGraph.js  # Graph topology state manager
│   ├── api/
│   │   └── client.js        # Axios instance with JWT interceptors
│   ├── types/               # Type definitions & prop-types
│   └── utils/               # Color interpolation, geometry, time formatting
```

## 2. Rendering the Signature Interactive Jigsaw Map
The Jigsaw Map is rendered using high-performance SVG (Scalable Vector Graphics) directly in React:
- **Junction Nodes:** Rendered as interactive circular SVG nodes with junction badges (`<circle>`, `<text>`).
- **Road Links:** Rendered as directed vector splines (`<path d="..." />`) with stroke widths corresponding to road capacity and stroke colors bound dynamically to real-time status (`GREEN` for Open, `CRIMSON` for Blocked).
- **Missing Puzzle Piece Effect:** When an edge is marked `BLOCKED`, the line transitions to an animated dashed pattern (`stroke-dasharray="8 6"`) with a red pulsating outline and a missing jigsaw puzzle cutout icon centered on the road link.
"""

docs["23_AUTHENTICATION_AND_ROLES.md"] = r"""# 23. Authentication and Roles

## 1. Security Architecture
The system employs stateless JSON Web Token (JWT) authentication using the HMAC-SHA256 (`HS256`) signing algorithm, paired with PBKDF2/Bcrypt password hashing (work factor 12).

## 2. User Roles & Permission Matrix

| Feature / Resource | Unauthenticated | Operator (`ROLE_OPERATOR`) | Admin (`ROLE_ADMIN`) |
| :--- | :---: | :---: | :---: |
| View Login Screen | Yes | Yes | Yes |
| View Live Dashboard & Telemetry | No | Read-Only | Read / Write |
| View CCTV Video Feeds | No | Read-Only | Read / Write |
| Trigger What-If Simulation | No | Yes | Yes |
| Calculate Alternative Detours | No | Yes | Yes |
| Acknowledge Alerts | No | Yes | Yes |
| Override Road Status Manually | No | Yes | Yes |
| Edit Camera Feeds & ROIs | No | No | Yes |
| Add / Delete Road Network Nodes | No | No | Yes |
| Adjust System Queue Thresholds | No | No | Yes |
| Manage User Accounts | No | No | Yes |

## 3. JWT Token Payload Example
```json
{
  "sub": "tanish_operator",
  "role": "ROLE_OPERATOR",
  "full_name": "Tanish Dhende",
  "exp": 1790707200,
  "iat": 1790678400
}
```
"""

docs["24_DASHBOARD_SPECIFICATION.md"] = r"""# 24. Dashboard Specification

## 1. Dashboard Layout Architecture
The main dashboard operates as the central cockpit for traffic surveillance and incident management.

```
+-----------------------------------------------------------------------------------------+
| [CROWD FLOW LOGO]   Pune Central TOC   [6 Cameras] [2 Congested] [1 Blocked] [Admin]    |
+-------------------------------------------------------------------+---------------------+
|                                                                   | SELECTED ROAD HUD   |
|                                                                   | Road: JM_ROAD_NORTH |
|                    DYNAMIC JIGSAW ROAD MAP                        | Status: CONGESTED   |
|                                                                   | Occupancy: 84%      |
|    [J1] ====(R1: Open)====> [J2] ====(R2: Slow)====> [J3]         | Avg Speed: 9 km/h   |
|      |                        |                        |          | Queue: 62m (14 veh) |
|      | (R4: Open)             | (R5: Open)             | (R3: ❌) |                     |
|      v                        v                        v          | [Mini CCTV Stream]  |
|    [J4] ====(R6: Detour) ==> [J5] ====(R7: Detour) => [J6]        |                     |
|                                                                   | [RUN SIMULATION]    |
|                                                                   | [MANUAL OVERRIDE]   |
+-------------------------------------------------------------------+---------------------+
| REAL-TIME ALERTS TICKER                                           | ADVISORY SUMMARY    |
| 19:31:02 - Alert: Road R3 Blocked (Pedestrian Protest detected)   | J05: +15s Green (NS)|
| 19:30:45 - Congestion on R2 (Queue persistence > 90s)             | J03: -10s Green (EW)|
+-------------------------------------------------------------------+---------------------+
```

## 2. Interactive Telemetry Widgets
1. **Network Health Ring:** Circular progress bar showing total network capacity utilization.
2. **Speed Distribution Gauge:** Real-time speedometer of average corridor velocity.
3. **Missing Jigsaw Notification Banner:** Flashing alert when an edge impedance becomes infinite.
"""

docs["25_CCTV_MONITORING_SPECIFICATION.md"] = r"""# 25. CCTV Monitoring Specification

## 1. Multi-Stream CCTV Interface
The CCTV Monitoring view displays up to 6 camera feeds concurrently in an adaptive responsive grid ($1 \times 1$, $2 \times 2$, or $3 \times 2$).

## 2. Real-Time Overlay Specification
Each camera viewport features hardware-accelerated HTML5 Canvas overlays:
- **Bounding Boxes:**
  - Cars: Neon Yellow (`#facc15`), $2\text{px}$ solid border.
  - Two-Wheelers: Electric Orange (`#fb923c`).
  - Heavy Vehicles (Buses/Trucks): Cyan (`#22d3ee`).
  - Pedestrians: Royal Purple (`#c084fc`).
- **Object Labels:** Text pill displaying `[ID: #142 | Car | 28 km/h]`.
- **ROI Boundary:** Translucent polygon with green border indicating the calibrated drivable road area.
- **Curbside Parking Boundary:** Dashed gray polygon marking the designated parking shoulder.
- **HUD Diagnostics Panel (Top-Right):**
  - Camera ID: `CAM_04_SWARGATE`
  - Stream Status: `LIVE (24.2 FPS)`
  - Active Vehicles inside ROI: `38`
  - Current Traffic State: `SIGNAL_QUEUE (Light RED: 14s remaining)`
"""

docs["26_DATA_FLOW.md"] = r"""# 26. Data Flow

## 1. End-to-End System Data Flow
The sequence below illustrates the life of a data frame from photon arrival at the CCTV lens to the generation of an advisory detour on the operator screen.

```mermaid
sequenceDiagram
    autonumber
    actor Driver as Urban Traffic
    participant CCTV as CCTV Camera
    participant CV as CV Pipeline (YOLO + Tracker)
    participant Feat as Feature Extractor
    participant State as Traffic State Engine
    participant Graph as Dynamic Jigsaw Graph
    participant Sim as Simulation Engine
    participant API as FastAPI Backend
    actor Operator as Traffic Operator (React UI)

    Driver->>CCTV: Movement on Road Segment R3
    CCTV->>CV: Ingest Video Frame (640x640)
    CV->>Feat: Bounding Boxes + Persistent Tracklets
    Feat->>State: Speed, Occupancy, Queue Persistence
    Note over State: Condition detected:<br/>Speed ~ 0 km/h, Occ > 85%,<br/>Queue Persist > 180s
    State->>Graph: Transition R3 to BLOCKED (Missing Piece)
    Graph->>Graph: Set Edge Cost W(R3) = INFINITY
    Graph->>API: Publish Road State Update & Alert
    API->>Operator: WebSocket Broadcast: [R3 BLOCKED]
    Operator->>Sim: Request What-If Redistribution
    Sim->>Graph: Query Adjacency & Capacities
    Sim-->>Operator: Render Before/After Redistribution Delta
    Operator->>Graph: Request Detour Route (J1 -> J6)
    Graph-->>Operator: Return Detour: J1 -> J4 -> J5 -> J6
```
"""

docs["27_UML_DIAGRAM_SPECIFICATION.md"] = r"""# 27. UML Diagram Specification

## 1. Class Diagram (Core Backend Domain)

```mermaid
classDiagram
    class RoadNode {
        +String nodeId
        +String name
        +Float x
        +Float y
        +List~RoadEdge~ outgoingEdges
    }

    class RoadEdge {
        +String roadId
        +String name
        +RoadNode source
        +RoadNode target
        +Float lengthMeters
        +Int lanes
        +Int capacityVph
        +Float freeFlowSpeed
        +RoadStatus currentStatus
        +Float dynamicCost
        +calculateImpedance() Float
        +setBlocked() void
    }

    class CameraFeed {
        +String cameraId
        +String streamUrl
        +RoadEdge monitoredRoad
        +List~Point~ roiPolygon
        +Float currentFps
        +processNextFrame() FrameObservation
    }

    class TrafficObservation {
        +DateTime timestamp
        +Int vehicleCount
        +Int pedestrianCount
        +Float averageSpeed
        +Float occupancyRatio
        +Float queuePersistence
        +TrafficState state
    }

    class JigsawGraphEngine {
        +Map~String, RoadNode~ nodes
        +Map~String, RoadEdge~ edges
        +updateEdgeObservation(obs) void
        +removeBlockedPiece(roadId) void
        +computeDijkstraPath(source, target) RouteResult
    }

    class WhatIfSimulator {
        +JigsawGraphEngine graph
        +simulateDisruption(blockedRoadId, volume) SimulationReport
    }

    RoadNode "1" *-- "many" RoadEdge : connects
    CameraFeed "1" --> "1" RoadEdge : monitors
    CameraFeed ..> TrafficObservation : generates
    RoadEdge "1" *-- "many" TrafficObservation : records
    JigsawGraphEngine "1" *-- "many" RoadNode : contains
    JigsawGraphEngine "1" *-- "many" RoadEdge : manages
    WhatIfSimulator --> JigsawGraphEngine : uses
```

## 2. Activity Diagram: Disruption Detection & Advisory Generation

```mermaid
flowchart TD
    A([Start Observation Cycle]) --> B[Ingest Video Frame]
    B --> C[Run YOLOv8 Object Detection]
    C --> D[Update Centroid Kalman Tracks]
    D --> E[Filter Objects within Lane ROI]
    E --> F[Extract Kinematic & Spatial Features]
    F --> G{Evaluate Rule Thresholds}
    G -- Normal / Flowing --> H[Set State: OPEN / SLOW]
    G -- Red Light Stop --> I[Set State: SIGNAL_QUEUE]
    G -- Persistent Jam / Blockage --> J[Set State: BLOCKED]
    H --> K[Update Dynamic Road Cost W_e]
    I --> K
    J --> L[Trigger Jigsaw Missing Piece Logic: W_e = inf]
    L --> M[Broadcast Critical Disruption Alert]
    M --> N[Recalculate Network Detour Routes]
    N --> O[Run What-If Redistribution Model]
    O --> P[Generate Advisory Signal Timing Splits]
    K --> Q([End Cycle / Publish Telemetry])
    P --> Q
```
"""

docs["28_ERROR_HANDLING.md"] = r"""# 28. Error Handling

## 1. Fail-Safe Architectural Tenets
A municipal traffic system must never experience catastrophic cascading crashes due to a single localized failure (e.g., an RTSP camera stream disconnecting or a malformed video file).

## 2. Handled Failure Scenarios

| Failure Scenario | Root Cause | System Response & Graceful Degradation |
| :--- | :--- | :--- |
| **Camera Feed Disconnect** | Network drop, IP camera reboot, file missing. | Pipeline catches connection timeout, logs error, displays "FEED OFFLINE" placeholder in UI, and marks road confidence as `DEGRADED`. The road retains its last known historical state or defaults to historical average. |
| **Zero Detections on Open Road** | Night conditions, temporary empty street. | Returns state `FREE_FLOW` with vehicle count 0; does not raise an exception or divide by zero. |
| **No Feasible Detour Route** | Multiple simultaneous blockages isolate a sub-graph. | Dijkstra detects unreachable target (`visited_costs[t] == inf`); API returns HTTP 200 with status `"NO_FEASIBLE_ROUTE"`, alerting the operator to dispatch manual traffic police intervention. |
| **Database Connection Failure** | SQLite lock contention or disk full. | Backend logs critical error, utilizes in-memory fallback state to continue serving live routing and video, and retries database transactions with exponential backoff. |
| **Model Inference Timeout** | CPU load spike on host laptop. | Frame-dropping mechanism skips current frame and advances to next keyframe; maintains API responsiveness without backlog buffering. |
"""

docs["29_LOGGING_AND_AUDITING.md"] = r"""# 29. Logging and Auditing

## 1. Structured Logging Specification
The system produces structured JSON logs via Python's standard `logging` library configured with an asynchronous queue handler:

```json
{
  "timestamp": "2026-09-29T19:35:12.104Z",
  "level": "INFO",
  "module": "traffic.state_engine",
  "camera_id": "CAM_02",
  "road_id": "ROAD_FC_04",
  "event": "STATE_TRANSITION",
  "old_state": "SLOW",
  "new_state": "CONGESTED",
  "metrics": {
    "occupancy": 0.82,
    "speed_kmh": 6.8,
    "queue_length_m": 54.0
  }
}
```

## 2. Audit Trail for Security & Operational Accountability
Every critical operator action is immutably recorded in the `AUDIT_LOGS` database table:
- **Manual Overrides:** When an operator forces a road state to `BLOCKED`.
- **Signal Implementations:** When an operator approves or dismisses an advisory signal split plan.
- **Configuration Modifications:** Changes to camera ROIs, lane capacities, or detection thresholds.
"""

docs["30_TESTING_STRATEGY.md"] = r"""# 30. Testing Strategy

## 1. Multi-Tier Testing Pyramid

```
       /\
      /  \     End-to-End System Tests (Playwright / Cypress)
     /----\    Integration Tests (Video Ingestion -> State -> Routing)
    /------\   Unit Tests (Pytest: Graph, Math, Dijkstra, Signal Splits)
```

## 2. Testing Frameworks & Tooling
- **Unit & Integration Testing:** `pytest`, `pytest-asyncio`, `pytest-cov`.
- **API Contract Testing:** `httpx` with FastAPI `TestClient`.
- **Mocking:** Synthetic video generation with OpenCV (drawing moving circles and rectangles to simulate vehicle flow and queues deterministically without needing real camera hardware during CI).

## 3. Test Coverage Goals
- **Graph & Routing Algorithms:** $100\%$ branch coverage (Dijkstra, infinite impedance, multi-path detour).
- **Traffic State Classification Rules:** $\ge 95\%$ coverage across all 8 traffic states.
- **API Endpoints:** $\ge 90\%$ coverage for authentication, routing, and simulation routers.
"""

for fname, content in docs.items():
    with open(os.path.join(docs_dir, fname), "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

print(f"Generated {len(docs)} documents successfully (Part 3).")
