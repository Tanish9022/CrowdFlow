# 08. UI Screen Specifications

## 1. Overview of Screen Hierarchy
The Crowd Flow frontend comprises 14 specialized operator screens:
1. **Login & Session Management** (`/login`)
2. **Main Command Dashboard** (`/`)
3. **Live CCTV Monitoring** (`/monitoring`)
4. **Traffic Analysis & Analytics** (`/analytics`)
5. **Jigsaw Network Map** (`/jigsaw-map`)
6. **Blocked Road Alert Center** (`/alerts`)
7. **Route Optimizer & Navigation** (`/routes`)
8. **What-If Disruption Simulator** (`/simulator`)
9. **Advisory Signal Recommendation** (`/signals`)
10. **Camera Inventory Management** (`/admin/cameras`)
11. **Road Network Graph Management** (`/admin/network`)
12. **Historical Traffic Replay** (`/history`)
13. **Audit Logs & Security** (`/admin/logs`)
14. **System Settings & Thresholds** (`/settings`)

## 2. Key Screen Specifications

### Screen 02: Main Command Dashboard
- **Header Top Bar:**
  - System Clock & Date (IST).
  - High-level KPIs: Active Cameras (e.g., 6/6 Online), Congested Corridors (e.g., 2), Blocked Roads (e.g., 1), Active Alerts (e.g., 3), Mean Network Saturation (e.g., 64%).
- **Central Canvas (65% width):**
  - Interactive SVG Jigsaw Map showing real-time road link colors and junction nodes.
  - Hovering on any link reveals an instant tooltip: `[Road ID: R03] | Count: 48 veh | Speed: 8 km/h | Occupancy: 88% | State: CONGESTED`.
- **Right Context Drawer (35% width):**
  - Selected Road Detail Card with mini live camera snapshot.
  - Speed vs. Occupancy real-time sparkline.
  - Instant one-click action: "Simulate Closure of this Road".
- **Bottom Summary Panel:**
  - Real-time ticker of system events and advisory notifications.

### Screen 03: Live CCTV Monitoring
- **Multi-Camera Grid:** $2 \times 2$ or $3 \times 2$ responsive grid of video feeds.
- **Video Canvas Overlays:**
  - Toggleable Bounding Boxes (Yellow = Car, Orange = Motorcycle, Cyan = Bus/Truck, Purple = Person).
  - Persistent Tracking ID badges above detected objects with instantaneous speed vectors.
  - Defined ROI polygon borders overlaid on the lane surface.
  - HUD overlay in upper left: `FPS: 24.2 | Count: 34 | State: SIGNAL_QUEUE (Light RED)`.
- **Operator Controls:** Play/Pause, Frame-Step, Camera Selection, Fullscreen Expand.

### Screen 05: Jigsaw Network Map
- **Visual Display:**
  - Geometric representation of road network with directed arrows indicating flow direction.
  - Segments colored dynamically (`GREEN` $\to$ `YELLOW` $\to$ `RED` $\to$ `CRIMSON`).
  - Blocked links render with a missing puzzle slot animation and flashing warning badge: `[BLOCKED: PIECE REMOVED]`.
  - Recalculated detour paths pulse in vibrant cyan with directional animation.\n


## 3. Screen Navigation Flow

`mermaid
flowchart TD
    LOGIN["/login - Authentication"] --> DASH["/ - Main Command Dashboard"]
    DASH --> MON["/monitoring - Live CCTV Grid"]
    DASH --> MAP["/jigsaw-map - Network Map"]
    DASH --> ROUTE["/routes - Route Optimizer"]
    DASH --> SIM["/simulator - What-If Simulator"]
    DASH --> SIG["/signals - Signal Advisory"]
    DASH --> ANALYTICS["/analytics - Traffic Analysis"]
    DASH --> ALERTS["/alerts - Blocked Road Alerts"]
    DASH --> SETTINGS["/settings - System Settings"]

    MON --> DASH
    MAP --> DASH
    ROUTE --> DASH
    SIM --> DASH
    SIG --> DASH
`

