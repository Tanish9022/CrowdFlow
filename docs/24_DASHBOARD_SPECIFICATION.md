# 24. Dashboard Specification

## 1. Dashboard Layout Architecture
The main dashboard operates as the central cockpit for traffic surveillance and incident management.

```text
+-----------------------------------------------------------------------------------------+
| [CROWD FLOW LOGO]   Pune Central TOC   [6 Cameras] [2 Congested] [1 Blocked] [Admin]    |
+-------------------------------------------------------------------+---------------------+
|                                                                   | SELECTED ROAD HUD   |
|                                                                   | Road: JM_ROAD_NORTH |
|                  REAL DIGITAL ROAD MAP OVERLAY                    | Status: CONGESTED   |
|                                                                   | Occupancy: 84%      |
|    📍[J1] ───🟢 (R1: Normal)──► 📍[J2] ───🟡 (R2: Slow)──► [J3]    | Avg Speed: 9 km/h   |
|       │                          │                     │          | Queue: 62m (14 veh) |
|       │ (R4: Normal)             │ (R5: Detour)        │ (R3: 🔴) |                     |
|       ▼                          ▼                     ▼          | [Mini CCTV Stream]  |
|    [J4] ───🟢 (R6: Detour) ───► [J5] ───🟢 (R7) ────► 📍[Dest]    |                     |
|                                                                   | [TOGGLE BLOCKAGE]   |
|                                                                   | [RUN SIMULATION]    |
+-------------------------------------------------------------------+---------------------+
| REAL-TIME DISRUPTION TICKER                                       | ADVISORY SUMMARY    |
| 🔴 CRITICAL: Road R03 (JM Road) is compromised by Protest Rally   | Deccan Jct: +15s NS |
| 🟢 Dynamic Detour Rerouting active via FC Road & Karve Corridor   | Swargate: +10s EW   |
+-------------------------------------------------------------------+---------------------+
```

## 2. Interactive Telemetry Widgets
1. **Real Digital Vector Map:** Displays Pune road geometry with live color-coded link saturation (🟢 Open/Recommended, 🟡 Slow, 🔴 Congested, ⚫ Blocked, 📍 Start/Destination pins, ➡️ Detour highlights).
2. **Network Health Ring:** Circular progress bar showing total network capacity utilization.
3. **Selected Link Drawer:** Inspection panel with live CCTV snapshot, speed metrics, occupancy ratio, and one-click manual block/reopen toggle.
4. **Advisory Signal Panel:** Synchronized green-split recommendations for downstream detour junctions.


## 3. Dashboard Component Layout

`mermaid
flowchart TD
    subgraph "Dashboard Page"
        subgraph "Top KPI Bar"
            A1["Active Cameras"]
            A2["Avg Network Speed"]
            A3["Bottleneck Corridors"]
            A4["Blocked Roads"]
        end

        subgraph "Main Grid - 70% + 30%"
            B1["Real Digital Road Map - Leaflet + OSM tiles"]
            B2["Selected Road HUD Drawer"]
        end

        subgraph "Bottom Panel"
            C1["Real-Time Disruption Log"]
            C2["Advisory Signal Plan Status"]
        end
    end

    B1 -- "Click road segment" --> B2
    B2 -- "Toggle Blockage" --> B1
    A4 -- "Count from" --> B1
`

