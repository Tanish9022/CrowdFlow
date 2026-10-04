# 29. Logging and Auditing

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


## Logging Architecture

`mermaid
flowchart LR
    subgraph "Event Sources"
        A1["API Requests"]
        A2["Auth Events"]
        A3["Road Status Changes"]
        A4["Simulation Runs"]
        A5["Signal Advisories"]
    end

    subgraph "Logging Pipeline"
        L1["Structured JSON Logger"]
        L2["Timestamp + Severity + Context"]
    end

    subgraph "Output"
        O1["Console - Development"]
        O2["Log File - Production"]
        O3["Audit Trail DB Table"]
    end

    A1 --> L1
    A2 --> L1
    A3 --> L1
    A4 --> L1
    A5 --> L1
    L1 --> L2
    L2 --> O1
    L2 --> O2
    L2 --> O3
`

