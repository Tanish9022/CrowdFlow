# 36. Demo Scenario

## 1. The Definitive SPPU Viva Demonstration Walkthrough
The end-to-end oral examination demo is structured as a clear 5-act narrative demonstrating every layer of the system:

### Act 1: Baseline Normal Network State
- Operator opens the dashboard (`http://localhost:5173`).
- All 6 road segments in the Pune Model Network show `GREEN (OPEN)` or `EMERALD (NORMAL)`.
- CCTV feeds display smooth simulated vehicular flow.
- A standard route query from Junction 1 to Junction 6 selects the direct corridor via Road $R_3$ (Total travel time: 3.5 minutes).

### Act 2: Sudden Disruption Event (Protest / Accident)
- On Road $R_3$ (JM Road North), a simulated protest rally or multi-vehicle collision occurs.
- CCTV feed for Camera 3 shows vehicles slowing to zero velocity, dense pedestrian clusters on the road, and queue persistence exceeding 120 seconds.
- The Traffic State Engine automatically flags Road $R_3$ as `BLOCKED`.
- Dashboard triggers a red alert ticker: **"CRITICAL DISRUPTION DETECTED: ROAD R3 (JM ROAD) COMPROMISED"**.

### Act 3: Dynamic Graph Recalculation & Real Map Rerouting
- The real digital road map instantly updates: Road $R_3$ turns black with a 🚧 roadblock marker.
- Dynamic impedance weight $W(R_3)$ is updated to $\infty$ in the backend graph engine.
- The route optimization engine recalculates the optimal path from Junction 1 to Junction 6: Road $R_3$ is avoided; the system highlights the new recommended green detour corridor via $J_1 \to J_4 \to J_5 \to J_6$ (Roads $R_4, R_6, R_7$).

### Act 4: What-If Redistribution Simulation
- The operator navigates to the Simulation tab to investigate downstream impact.
- Clicks "Simulate Disruption: 100% of R3 Flow Diverted".
- The simulation engine renders the comparative before-and-after view:
  - Road $R_6$ occupancy jumps from $35\%$ to $86\%$ (`CONGESTED`).
  - Junction 5 approach experiences extreme queue pressure.

### Act 5: Advisory Signal Rebalancing
- The system automatically generates an Advisory Signal Timing Plan for Junction 5:
  - North-South green phase increased from $35\text{ s}$ to $55\text{ s}$ (+20s).
  - Cross-street green phase adjusted to maintain cycle balance.
- Operator clicks "Acknowledge & Implement Advisory".
- Summary telemetry shows simulated detour delay reduced by $38\%$.


## 2. Demo Flow Sequence

`mermaid
sequenceDiagram
    actor Examiner as SPPU Examiner
    actor Operator as Demo Operator
    participant UI as React Dashboard
    participant API as FastAPI Backend
    participant Graph as Jigsaw Graph Engine
    participant Sim as Simulation Engine
    participant Sig as Signal Advisory Engine

    Note over Examiner,Sig: Act 1 - Baseline Normal State
    Operator->>UI: Open Dashboard
    UI->>API: GET /network/graph
    API-->>UI: All roads GREEN/OPEN
    UI-->>Examiner: All roads shown green on real map

    Note over Examiner,Sig: Act 2 - Sudden Disruption
    Operator->>UI: Click Road R3, Mark as BLOCKED
    UI->>API: PATCH /network/roads/R3/status BLOCKED
    API->>Graph: Set W(R3) = infinity
    API-->>UI: Road R3 turns black, alert triggered
    UI-->>Examiner: Red alert ticker appears

    Note over Examiner,Sig: Act 3 - Dynamic Rerouting
    Operator->>UI: Request route J1 to J6
    UI->>API: POST /routing/calculate
    API->>Graph: Dijkstra avoiding R3
    API-->>UI: Detour via J1-J4-J5-J6
    UI-->>Examiner: Green detour highlighted on map

    Note over Examiner,Sig: Act 4 - What-If Simulation
    Operator->>UI: Run simulation for R3 closure
    UI->>API: POST /simulation/run
    API->>Sim: Redistribute R3 volume
    Sim-->>API: Before/After delta
    API-->>UI: Show occupancy changes
    UI-->>Examiner: R6 jumps to 86% CONGESTED

    Note over Examiner,Sig: Act 5 - Signal Advisory
    API->>Sig: Generate advisory for Junction 5
    Sig-->>API: NS green +20s, EW green -18s
    API-->>UI: Advisory signal plan
    Operator->>UI: Acknowledge advisory
    UI-->>Examiner: Delay reduced by 38%
`

