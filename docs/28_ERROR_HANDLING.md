# 28. Error Handling

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


## Error Handling Strategy

`mermaid
flowchart TD
    REQ["API Request"] --> MW["Middleware Layer"]
    MW --> TRY{"Try Execute"}
    TRY -- Success --> RES["JSON Response 200"]
    TRY -- ValidationError --> E1["422 Unprocessable Entity"]
    TRY -- AuthError --> E2["401 Unauthorized"]
    TRY -- NotFound --> E3["404 Not Found"]
    TRY -- DBError --> E4["500 Internal Server Error"]
    TRY -- Timeout --> E5["504 Gateway Timeout"]

    E1 --> LOG["Structured Error Logging"]
    E2 --> LOG
    E3 --> LOG
    E4 --> LOG
    E5 --> LOG
    LOG --> RETRY{"Retryable?"}
    RETRY -- Yes --> BACK["Exponential Backoff"]
    RETRY -- No --> ALERT["Alert Operator"]
`

