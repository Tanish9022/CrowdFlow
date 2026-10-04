# 19. Database Design

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
