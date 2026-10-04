# 24. Dashboard Specification

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
