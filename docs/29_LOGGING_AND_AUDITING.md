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
