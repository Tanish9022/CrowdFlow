# 26. Data Flow

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
