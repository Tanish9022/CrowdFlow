# 31. Test Cases

## 1. Test Suite Matrix
The following formal test cases validate the core functional and algorithmic components of Crowd Flow.

| Test ID | Module | Scenario / Input | Expected Result | Pass Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **TC-CV-01** | Detector | Video with 12 cars, 8 bikes, 2 buses. | All 22 vehicles detected with class labels. | Count accuracy $\ge 90\%$. |
| **TC-CV-02** | Tracker | Occluded vehicle passes behind a bus. | `track_id` maintained after emerging. | Track persistence across occlusions. |
| **TC-ROI-01** | Spatial | Parked cars outside road polygon ROI. | Vehicles excluded from active road density. | Road occupancy unaffected by off-road cars. |
| **TC-TRF-01**| State Engine| $v = 45\text{ km/h}$, occupancy $= 15\%$. | Classified as `FREE_FLOW`. | Exact state match. |
| **TC-TRF-02**| State Engine| $v = 0\text{ km/h}$, signal = `RED`, $t = 20\text{ s}$. | Classified as `SIGNAL_QUEUE`. | Distinguishes red light from traffic jam. |
| **TC-TRF-03**| State Engine| $v = 1.2\text{ km/h}$, $t_{\text{persist}} = 210\text{ s}$. | Classified as `HEAVY_CONGESTION` / `BLOCKED`. | Identifies prolonged non-clearing bottleneck. |
| **TC-GRP-01**| Jigsaw Graph| Edge $R_3$ status changed to `BLOCKED`. | $W(R_3) = \infty$, edge skipped in traversal. | Zero traffic routed through $R_3$. |
| **TC-ROT-01**| Dijkstra | Query path between $J_1$ and $J_6$ with $R_3$ blocked. | Computes detour via $J_4 \to J_5 \to J_6$. | Shortest alternative path without cycle. |
| **TC-SIM-01**| What-If Sim | Divert $1000\text{ vph}$ from $R_3$ to parallel $R_4, R_5$. | Flow distributed proportionally to residual capacity. | Total displaced volume conserved. |
| **TC-SIG-01**| Signal Advisory| Detour approach volume surges from 300 to 900 vph. | Green phase recommendation increases (e.g., $+20\text{ s}$). | Rebalanced split within safety limits ($15\text{ s} \le g \le 70\text{ s}$). |
| **TC-API-01**| Security | Request `/api/v1/network/roads` without JWT token. | HTTP 401 Unauthorized returned. | Authentication enforced. |
