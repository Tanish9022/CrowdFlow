# 03. User Roles and Use Cases

## 1. User Roles

### 1.1 Traffic Police Control Room Operator (`ROLE_OPERATOR`)
- **Profile:** Field officers and desk operators at Pune City Traffic Police Command Center.
- **Responsibilities:**
  - Continuously monitor live CCTV feeds and alert feeds.
  - Review AI-detected road blockages and verify incidents.
  - Inspect recommended detour corridors and signal split suggestions.
  - Issue manual overrides (e.g., mark a road as blocked based on emergency phone calls).
- **Access Level:** Read-only CCTV, trigger What-If simulation, execute route calculations, acknowledge alerts.

### 1.2 Traffic Engineer / Systems Administrator (`ROLE_ADMIN`)
- **Profile:** Municipal traffic planning engineers and system maintainers.
- **Responsibilities:**
  - Configure camera streams (RTSP/video file paths, ROI coordinates, perspective calibration).
  - Define and update the road network graph (nodes, edges, lane capacities, baseline free-flow speeds).
  - Adjust threshold parameters for queue persistence, occupancy limits, and congestion alarms.
  - Manage user credentials and audit system operational logs.
- **Access Level:** Full CRUD access to cameras, road graph, signal plans, and user management.

## 2. Core Use Cases

```mermaid
usecaseDiagram
    actor Operator as "Traffic Operator"
    actor Admin as "Traffic Engineer/Admin"

    package "Crowd Flow System" {
        usecase UC1 as "UC-1: Monitor Live CCTV Feeds & Overlays"
        usecase UC2 as "UC-2: Detect & Verify Road Blockage"
        usecase UC3 as "UC-3: Run What-If Disruption Simulation"
        usecase UC4 as "UC-4: View Recommended Detour Routes"
        usecase UC5 as "UC-5: Review Advisory Signal Timing Plan"
        usecase UC6 as "UC-6: Configure Road Graph & Junctions"
        usecase UC7 as "UC-7: Calibrate Camera ROI & Lanes"
        usecase UC8 as "UC-8: Inspect Historical Traffic Logs"
    }

    Operator --> UC1
    Operator --> UC2
    Operator --> UC3
    Operator --> UC4
    Operator --> UC5
    Operator --> UC8

    Admin --> UC1
    Admin --> UC6
    Admin --> UC7
    Admin --> UC8
```

### Detailed Use Case Descriptions

#### UC-2: Detect & Verify Road Blockage
- **Primary Actor:** Traffic Operator
- **Preconditions:** Camera feed is active, background AI inference is running.
- **Flow of Events:**
  1. CCTV pipeline detects persistent stationary vehicles across all lanes of Road Edge $E_{12}$ for $t > 120	ext{ s}$, with zero downstream departure rate.
  2. Traffic State Engine transitions $E_{12}$ state from `CONGESTED` to `BLOCKED`.
  3. Dashboard triggers an audio-visual Jigsaw Disruption Alert.
  4. Operator views highlighted camera snapshot and verifies that an overturned truck or protest is blocking the road.
  5. Operator confirms the blockage state; the graph engine immediately removes $E_{12}$ from active routing.
- **Postconditions:** All subsequent route queries bypass $E_{12}$; What-If simulation computes spillover to roads $E_{14}$ and $E_{15}$.

#### UC-3: Run What-If Disruption Simulation
- **Primary Actor:** Traffic Operator / Traffic Engineer
- **Preconditions:** Network graph is populated with current traffic density estimates.
- **Flow of Events:**
  1. Operator navigates to the Simulation tab.
  2. Selects target road (e.g., "JM Road Segment 3") and disruption scenario (e.g., "Protest / Gathering - Complete Closure").
  3. Sets projected duration (e.g., 60 minutes) and expected diverted volume (default: 100% of upstream flow).
  4. Clicks "Execute Simulation".
  5. System calculates diverted flow distribution across alternative corridors using capacity-impedance redistribution.
  6. UI renders side-by-side comparison: Before vs. After occupancy, saturated edges highlighted in red, and bottleneck delay estimates.\n