# 20. API Specification

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


## 3. API Request Flow

`mermaid
sequenceDiagram
    actor Operator as Traffic Operator
    participant UI as React Frontend
    participant API as FastAPI Backend
    participant Auth as JWT Auth Middleware
    participant DB as SQLite Database
    participant Graph as Jigsaw Graph Engine

    Operator->>UI: Login with credentials
    UI->>API: POST /api/v1/auth/login
    API->>Auth: Validate credentials
    Auth-->>API: Return JWT token
    API-->>UI: Bearer token

    Operator->>UI: Open Dashboard
    UI->>API: GET /api/v1/network/graph
    API->>Auth: Verify JWT
    Auth-->>API: Authorized
    API->>Graph: Fetch current topology
    Graph-->>API: Nodes, edges, statuses
    API-->>UI: JSON network response
    UI-->>Operator: Render real digital road map

    Operator->>UI: Click road to block
    UI->>API: PATCH /api/v1/network/roads/{id}/status
    API->>Graph: Update edge cost to infinity
    API->>DB: Persist status change
    API-->>UI: Updated road state
    UI-->>Operator: Road turns black on map
`

