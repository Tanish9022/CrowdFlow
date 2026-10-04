import os

docs_dir = "docs"

docs = {}

docs["01_PROJECT_VISION.md"] = """# 01. Project Vision

## 1. Executive Summary
**Crowd Flow** is an AI-based traffic and route management decision-support prototype that monitors urban road networks through CCTV video feeds, detects traffic bottlenecks, represents the road grid as an adaptive "jigsaw" graph, and simulates the ripple effects of road closures. When a road is compromised by protests, VIP movements, accidents, waterlogging, or severe congestion, Crowd Flow treats that road as a missing puzzle piece, recalculates alternative routes avoiding saturated links, simulates the redistribution of displaced vehicles, and recommends optimized traffic signal splits for traffic police operators.

## 2. Academic & Institutional Context
- **Institution:** Savitribai Phule Pune University (SPPU)
- **Degree:** Bachelor of Science in Computer Science (T.Y. B.Sc. CS)
- **Course Code:** CS-331-FP (Project Work)
- **Academic Year:** 2025–2026 / 2026–2027
- **Project Team:**
  - Tanish Dhende (Roll No. 98)
  - Palavi Jadhav (Roll No. 108)

## 3. Core Philosophy: The Dynamic Jigsaw Metaphor
Traditional navigation applications (such as Google Maps or MapmyIndia) treat road navigation from an egocentric point of view: finding the fastest path for a single driver without considering systemic capacity constraints. When a major arterial corridor closes, naive rerouting dumps thousands of vehicles onto narrow residential feeder roads, causing secondary gridlock.

Crowd Flow models the urban traffic network as a **dynamic jigsaw puzzle**:
1. **Nodes (Intersections):** Fixed vertices where traffic splits or converges.
2. **Edges (Road Segments):** Dynamic jigsaw pieces with finite physical vehicle capacities, current densities, and flow rates.
3. **Missing Piece (Disruption Event):** When a segment is blocked, that piece is removed from the usable graph.
4. **Jigsaw Fit (Traffic Redistribution):** Traffic cannot vanish; the volume displaced from the missing piece must be distributed across remaining corridors without exceeding critical capacity thresholds ($V/C > 0.85$).
5. **Advisory Rebalancing:** To assist the newly loaded detour corridors, the system generates signal timing advisories (e.g., extending green phase time along detour arterial corridors).

## 4. Key Distinctions
| Feature | Generic CCTV Project | Standard Navigation App | Crowd Flow Academic System |
| :--- | :--- | :--- | :--- |
| **Primary Goal** | Count vehicles in a frame | Reroute single vehicle | Network-wide traffic balance & decision support |
| **AI Role** | Object detection bounding boxes | GPS probe aggregation | Spatial-temporal tracking, queue persistence, road state classification |
| **Graph Dynamics** | Static or nonexistent | Commercial proprietary API | Explicit directed graph with real-time capacity-impedance functions |
| **Disruption Handling** | None | Reactive rerouting | Proactive "What-If" redistribution simulation |
| **Signal Control** | None | None | Capacity-aware advisory signal phase splits |

## 5. System Statement
> "Crowd Flow converts CCTV observations into a dynamic representation of a road network. It detects and tracks vehicles, extracts movement and queue features, determines the state of individual roads, and represents those roads as a dynamic graph. When a road becomes blocked or overloaded, the system treats it as a missing piece in the traffic jigsaw, recalculates feasible routes through the remaining network, simulates traffic redistribution, and generates route and signal recommendations for an operator."
"""

docs["02_PROBLEM_STATEMENT_AND_OBJECTIVES.md"] = """# 02. Problem Statement and Objectives

## 1. Problem Statement
Urban traffic management in developing metropolitan areas (such as Pune and Mumbai under SPPU jurisdiction) faces recurring crises due to sudden disruptions: public rallies, religious processions, unplanned construction, waterlogging during monsoons, and fatal traffic collisions.

Existing traffic surveillance systems in municipal command centers suffer from three major shortcomings:
1. **Visual Overload:** Hundreds of CCTV screens are monitored manually by human operators, leading to delayed detection of queue build-ups and road blockages.
2. **Detection vs. Intelligence Disconnect:** Conventional computer vision demos display bounding boxes around cars but fail to translate pixel detections into actionable traffic metrics (such as road occupancy percentage, queue persistence, and spatial-temporal stagnation).
3. **Lack of Predictive Redistribution:** When an arterial road is shut down, police deploy barricades reactively without predictive insights into how adjacent secondary roads will absorb the diverted vehicle volume, leading to cascade congestion across neighboring junctions.

## 2. Project Objectives

### Primary Objectives
1. **Automated Vision Pipeline:** Develop an edge-feasible computer vision pipeline using lightweight YOLO object detection combined with multi-object tracking (ByteTrack/centroid tracking) to calculate vehicle counts, average velocity, spatial occupancy, and stationary duration from CCTV camera feeds.
2. **Traffic-State Classification Engine:** Formulate deterministic, rule-based and machine-learning feature classification that accurately distinguishes between:
   - Free Flow
   - Normal Traffic
   - Slow Moving Traffic
   - Signal-Induced Queues (transient red light stops)
   - Heavy Congestion / Persistent Bottlenecks
   - Roadside Parked Vehicles
   - Pedestrian Crowds / Processions
3. **Dynamic Jigsaw Graph Architecture:** Construct a directed mathematical graph $G = (V, E)$ where nodes represent road junctions and edges represent road corridors with dynamic impedance cost functions derived from real-time CCTV metrics.
4. **Adaptive Route Optimization:** Implement modified Dijkstra / A* pathfinding that penalizes heavily congested segments and treats physically blocked or severed edges as having infinite impedance ($\infty$), immediately generating alternative detour paths.
5. **What-If Traffic Redistribution Simulation:** Build a transparent, explainable macroscopic traffic redistribution simulator that models how vehicle volume from a disabled road disperses across parallel links according to capacity elasticity.
6. **Advisory Signal Rebalancing:** Provide actionable recommendations for traffic signal cycle times (green split adjustments) at downstream intersections to accommodate diverted traffic surges.
7. **Unified Operator Dashboard:** Present an intuitive, high-performance web dashboard displaying real-time video overlays, network graph topology, jigsaw disruption alerts, and before-and-after simulation analytics.

## 3. Measurable Success Criteria
- Vehicle detection and tracking running at $\ge 12-15$ FPS on a modern quad-core CPU (Intel i3/i5) without requiring dedicated discrete GPUs.
- Accurate differentiation between signal queues (dispersing when light turns green) and persistent congestion queues with $>90\%$ simulated rule fidelity.
- Sub-50ms recalculation of alternative routes for a 20-node, 40-edge urban test network upon road closure.
- Zero reliance on external paid mapping APIs (Google Maps API, Mapbox) for core routing and graph operations.
"""

docs["03_USER_ROLES_AND_USE_CASES.md"] = """# 03. User Roles and Use Cases

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
  1. CCTV pipeline detects persistent stationary vehicles across all lanes of Road Edge $E_{12}$ for $t > 120\text{ s}$, with zero downstream departure rate.
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
  6. UI renders side-by-side comparison: Before vs. After occupancy, saturated edges highlighted in red, and bottleneck delay estimates.
"""

docs["04_SCOPE_LIMITATIONS_AND_FEASIBILITY.md"] = """# 04. Scope, Limitations, and Feasibility

## 1. Project Scope

### In-Scope Deliverables
1. **Video Ingestion:** Ingestion of pre-recorded traffic CCTV footage (MP4/AVI) and live local webcams or RTSP simulation feeds.
2. **Object Detection & Tracking:** Detection of five core urban mobility classes: `car`, `motorcycle`, `bus`, `truck`, and `person` using lightweight YOLO models (`yolov8n`).
3. **Traffic Feature Extraction:** Calculation of per-frame vehicle count, average velocity (pixel displacement calibrated to km/h), road occupancy percentage, stationary vehicle count, and queue persistence time.
4. **Traffic State Engine:** Seven state classifications: `FREE_FLOW`, `NORMAL`, `SLOW`, `SIGNAL_QUEUE`, `TRAFFIC_QUEUE`, `HEAVY_CONGESTION`, `PARKED`, and `PEDESTRIAN_CROWD`.
5. **Graph Representation:** Directed graph representing an urban sector (e.g., 10–25 nodes, 20–50 road segments) with dynamic edge weights.
6. **Dynamic Routing:** Recalculation of optimal routes using Dijkstra's algorithm with dynamic impedance incorporating distance, occupancy, and congestion penalties.
7. **What-If Simulation:** Macroscopic capacity-constraint redistribution modeling the systemic impact of road closures.
8. **Signal Timing Recommendation:** Cycle and green split recommendations for affected intersections to prevent detour gridlock.
9. **Full-Stack Application:** FastAPI backend with SQLite/PostgreSQL database, and React frontend dashboard.

### Out-of-Scope (Explicit Non-Goals)
1. **Direct Hardware Signal Actuation:** The system **NEVER** issues direct electrical or programmatic commands to physical roadside traffic controllers (e.g., SCATS, SCOOT, or physical relays). All signal outputs are strictly designated as **Advisory Recommendations**.
2. **City-Scale Microscopic Physics Simulation:** Crowd Flow is not a replacement for multi-gigabyte microscopic simulation suites like SUMO, VISSIM, or AIMSUN. It uses an explainable macroscopic redistribution model.
3. **Automated Number Plate Recognition (ANPR) / Chalan Generation:** The system does not identify individual vehicles, owners, or traffic violations.
4. **General Navigation Mobile App:** Crowd Flow is designed for municipal traffic control room operators, not consumer drivers on mobile phones.

## 2. Technical Limitations
- **Camera Perspective & Occlusion:** Extreme camera angles or heavy rain/fog can degrade detection accuracy. Calibration relies on user-defined Region-of-Interest (ROI) polygons.
- **Speed Calibration:** Without camera intrinsic calibration and GPS ground truth, speeds are estimated via homography or pixel-to-meter scaling factors.
- **Hardware Constraints:** On dual-core or low-power CPUs without GPU acceleration, YOLO inference may operate at 5–10 FPS; frame-skipping techniques are implemented to maintain real-time responsiveness.

## 3. Feasibility Analysis

### Technical Feasibility
- Modern lightweight models like YOLOv8 Nano (`yolov8n.pt`) have only 3.2 million parameters and run at >30 FPS on standard CPUs using ONNX Runtime or PyTorch CPU.
- Graph algorithms (Dijkstra) for graphs under 1,000 nodes execute in less than 5 milliseconds in pure Python.
- Modern web stacks (FastAPI + React) run seamlessly on low-resource machines.

### Economic Feasibility
- 100% open-source software stack: Python, OpenCV, Ultralytics, FastAPI, SQLite, React, Leaflet/SVG.
- Zero licensing costs, zero proprietary cloud API dependencies.

### Operational Feasibility (SPPU Viva Context)
- Highly demonstrable on a standard student laptop during oral examination.
- Every mathematical step (graph cost, queue formula, green split advisory) is transparent and explainable to examiners.
"""

docs["05_SYSTEM_REQUIREMENTS.md"] = """# 05. System Requirements

## 1. Hardware Requirements

### Minimum Requirements (Target Demonstration Laptop)
- **Processor:** Intel Core i3 (7th Gen or newer) or AMD Ryzen 3
- **Clock Speed:** 2.0 GHz or higher (Dual-Core with Hyperthreading)
- **RAM:** 8 GB DDR4
- **Storage:** 10 GB available SSD/HDD storage (for dataset clips, Python virtual environment, dependencies)
- **Display Resolution:** $1366 \\times 768$ pixels
- **Input:** Standard Keyboard, Mouse / Trackpad

### Recommended Requirements (Optimal Performance)
- **Processor:** Intel Core i5 / i7 (10th Gen or newer) or AMD Ryzen 5 / 7
- **RAM:** 16 GB DDR4/DDR5
- **GPU (Optional):** NVIDIA GeForce GTX 1650 / RTX 3050 (4 GB VRAM) with CUDA support
- **Display Resolution:** $1920 \\times 1080$ Full HD
- **Storage:** 20 GB available NVMe SSD storage

## 2. Software Requirements

### Operating System
- Microsoft Windows 10 (64-bit) or Windows 11 (64-bit)
- Compatible with Ubuntu Linux 22.04 LTS / 24.04 LTS

### Runtime Environments & Compilers
- **Python:** Version 3.10.x to 3.12.x (64-bit)
- **Node.js:** Version 18.x LTS to 22.x LTS
- **Package Managers:** `pip` (Python), `npm` (Node.js)

### Core Libraries & Frameworks

#### Backend & Machine Learning
- `fastapi` $\\ge 0.110.0$ (High performance ASGI Web API framework)
- `uvicorn[standard]` $\\ge 0.28.0$ (ASGI web server)
- `ultralytics` $\\ge 8.1.0$ (YOLOv8 object detection)
- `opencv-python-headless` $\\ge 4.9.0$ (Computer vision and video frame processing)
- `numpy` $\\ge 1.26.0$ (Vectorized array calculations)
- `scipy` $\\ge 1.12.0$ (Spatial calculations, Hungarian algorithm)
- `networkx` $\\ge 3.2.0$ (Graph modeling and shortest path verification)
- `sqlalchemy` $\\ge 2.0.0$ (ORM for relational database management)
- `pydantic` $\\ge 2.6.0$ (Data validation and API schemas)
- `python-jose[cryptography]` $\\ge 3.3.0$ (JWT token authentication)
- `passlib[bcrypt]` $\\ge 1.7.4$ (Password hashing)

#### Frontend & UI
- `react` $\\ge 18.2.0$
- `react-dom` $\\ge 18.2.0$
- `react-router-dom` $\\ge 6.22.0$
- `lucide-react` (Clean engineering iconography)
- `recharts` $\\ge 2.12.0$ (Data analytics and telemetry charts)
- Modern Vanilla CSS with CSS Custom Properties (Theme Design System)

## 3. Network Requirements
- Fully self-contained offline capability: System runs entirely on `localhost` (`127.0.0.1:8000` for backend, `127.0.0.1:5173` or `3000` for frontend).
- No continuous external internet connection required during examination viva.
"""

docs["06_TECH_STACK_AND_ARCHITECTURE.md"] = """# 06. Tech Stack and Architecture

## 1. Architectural Philosophy
Crowd Flow follows a **Modular Clean Architecture** pattern designed to separate computer vision perception from higher-level graph algorithms and user interfaces. This decoupling ensures that edge camera failures or model updates do not disrupt graph routing or operator dashboard functionality.

## 2. High-Level Architectural Diagram

```mermaid
graph TD
    subgraph "Perception Layer"
        CAM[CCTV Video Streams / MP4 Feeds] --> DECODE[OpenCV Frame Ingestion]
        DECODE --> DET[YOLOv8 Object Detector]
        DET --> TRACK[ByteTrack / Centroid Tracker]
        TRACK --> ROI[Lane ROI Filter & Homography]
        ROI --> FEAT[Traffic Feature Extractor]
    end

    subgraph "Intelligence & Decision Layer"
        FEAT --> STATE[Traffic State Classifier]
        STATE --> JIGSAW[Dynamic Jigsaw Graph Engine]
        JIGSAW --> ROUTE[Dijkstra Dynamic Route Optimizer]
        JIGSAW --> SIM[What-If Traffic Redistribution Simulator]
        SIM --> SIG[Advisory Signal Timing Engine]
    end

    subgraph "Storage & Communication Layer"
        DB[(SQLite / PostgreSQL Database)]
        STATE <--> DB
        JIGSAW <--> DB
        SIG <--> DB
        API[FastAPI REST & WebSocket Endpoints]
        STATE --> API
        JIGSAW --> API
        ROUTE --> API
        SIM --> API
        SIG --> API
    end

    subgraph "Presentation Layer"
        API <--> DASH[React Operator Dashboard]
        DASH --> VIZ1[Live CCTV Video & Bounding Overlays]
        DASH --> VIZ2[Interactive Jigsaw Network Map]
        DASH --> VIZ3[What-If Redistribution Comparison]
        DASH --> VIZ4[Advisory Signal Split Panel]
    end
```

## 3. Technology Selection Rationale

| Layer | Chosen Technology | Alternatives Considered | Selection Justification |
| :--- | :--- | :--- | :--- |
| **Object Detection** | YOLOv8 Nano (`yolov8n`) | Faster R-CNN, SSD, YOLOv5 | Ultra-lightweight (3.2M params), excellent CPU inference speeds (~30-50ms), native PyTorch/ONNX support. |
| **Tracking** | ByteTrack / IoU Centroid | DeepSORT, StrongSORT | ByteTrack retains low-confidence detections from occluded vehicles without requiring heavy secondary feature extraction CNNs. |
| **Backend Framework**| FastAPI (Python 3.12) | Django, Flask, Express.js | Async capability, native Pydantic validation, auto-generated OpenAPI documentation, fast execution. |
| **Graph Operations** | Custom Python Engine + NetworkX | Neo4j, pgRouting | In-memory graph operations ensure sub-millisecond route recalculation without heavy database overhead. |
| **Database** | SQLite (dev) / PostgreSQL (prod)| MongoDB, Redis | ACID compliance for relational graph nodes, edges, logs, and zero-configuration portability for academic viva. |
| **Frontend** | React 18 + Modern CSS | Next.js, Vue, Angular | Modular component architecture, direct DOM control for custom SVG jigsaw map rendering, zero bloat. |
"""

docs["07_UI_UX_DESIGN_SYSTEM.md"] = """# 07. UI/UX Design System

## 1. Visual Language & Design Theme
Crowd Flow is designed as an **Industrial Municipal Traffic Operations Command Center (TOC)** dashboard. It avoids generic, bright corporate templates in favor of a focused, high-contrast **Obsidian Control Room** dark theme.

The visual language communicates:
- **Real-Time Responsiveness:** Pulsing status indicators, live telemetry readouts.
- **Safety Criticality:** High-contrast semantic traffic colors (Green = Open, Amber = Slow/Queue, Red = Congested, Crimson = Blocked).
- **Spatial Intelligence:** Custom vector-rendered Jigsaw road topology.

## 2. Color Palette & Design Tokens

```css
:root {
  /* Surface & Background Colors */
  --bg-primary: #0a0e17;       /* Deep obsidian canvas */
  --bg-secondary: #111827;     /* Elevated control panels */
  --bg-tertiary: #1f2937;      /* Hover surfaces & borders */
  --bg-card: rgba(17, 24, 39, 0.85); /* Glassmorphic card surface */

  /* Text & Typography */
  --text-primary: #f9fafb;     /* High-contrast crisp white */
  --text-secondary: #9ca3af;   /* Muted labels & subtitles */
  --text-muted: #6b7280;       /* Timestamps & minor legends */

  /* Semantic Traffic State Colors */
  --traffic-open: #10b981;      /* Emerald Green (Free Flow) */
  --traffic-slow: #f59e0b;      /* Amber / Orange (Reduced Speed) */
  --traffic-queue: #eab308;     /* Signal-induced queue (Yellow) */
  --traffic-congested: #ef4444; /* Bright Red (Over capacity) */
  --traffic-blocked: #dc2626;   /* Deep Crimson / Flashing (Missing Jigsaw Piece) */
  --traffic-crowd: #8b5cf6;     /* Purple (Pedestrian surge / Protest) */

  /* Accent & Action Colors */
  --accent-cyan: #06b6d4;      /* Telemetry, tracking IDs, graphs */
  --accent-blue: #3b82f6;      /* Primary action buttons */
  --accent-glow: rgba(6, 182, 212, 0.25);

  /* Borders & Dividers */
  --border-subtle: #1f2937;
  --border-active: #374151;
  --border-focus: #06b6d4;
}
```

## 3. Typography
- **Primary Interface Font:** `Inter`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `Roboto`, sans-serif.
- **Monospace Telemetry Font:** `JetBrains Mono`, `Fira Code`, `Consolas`, monospace (used for FPS, vehicle counts, coordinates, and cost scores).
- **Scale:**
  - Display Title: 24px / 1.2 / Semi-Bold (Dashboard Headers)
  - Section Title: 18px / 1.3 / Medium (Widget Headers)
  - Card Value: 28px / 1.1 / Bold (Metrics: Vehicle count, Speed, Delay)
  - Body Text: 14px / 1.5 / Regular
  - Meta/Caption: 12px / 1.4 / Regular (Status labels, timestamps)

## 4. UI Component Guidelines
1. **Cards & Widgets:** Rounded corners ($8\\text{px}$), subtle glassmorphism border (`1px solid var(--border-subtle)`), deep drop shadows (`0 4px 20px rgba(0,0,0,0.4)`).
2. **Jigsaw Road Rendering:** Road segments rendered with thick SVG paths ($6\\text{px}-10\\text{px}$) colored by their dynamic state. Blocked segments render with dashed animated borders or missing cutouts.
3. **Buttons & Controls:** Clear hover transitions (200ms ease), focused accessibility outlines, disabled states clearly marked with 50% opacity and `cursor: not-allowed`.
4. **Alert Banners:** Non-intrusive sticky top/side notifications with dismiss and "Investigate on Map" deep-links.
"""

docs["08_UI_SCREEN_SPECIFICATIONS.md"] = """# 08. UI Screen Specifications

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
- **Multi-Camera Grid:** $2 \\times 2$ or $3 \\times 2$ responsive grid of video feeds.
- **Video Canvas Overlays:**
  - Toggleable Bounding Boxes (Yellow = Car, Orange = Motorcycle, Cyan = Bus/Truck, Purple = Person).
  - Persistent Tracking ID badges above detected objects with instantaneous speed vectors.
  - Defined ROI polygon borders overlaid on the lane surface.
  - HUD overlay in upper left: `FPS: 24.2 | Count: 34 | State: SIGNAL_QUEUE (Light RED)`.
- **Operator Controls:** Play/Pause, Frame-Step, Camera Selection, Fullscreen Expand.

### Screen 05: Jigsaw Network Map
- **Visual Display:**
  - Geometric representation of road network with directed arrows indicating flow direction.
  - Segments colored dynamically (`GREEN` $\\to$ `YELLOW` $\\to$ `RED` $\\to$ `CRIMSON`).
  - Blocked links render with a missing puzzle slot animation and flashing warning badge: `[BLOCKED: PIECE REMOVED]`.
  - Recalculated detour paths pulse in vibrant cyan with directional animation.
"""

docs["09_CCTV_AI_PIPELINE.md"] = """# 09. CCTV AI Pipeline

## 1. Perception Pipeline Overview
The CCTV AI Pipeline processes raw uncompressed video frames, identifies and tracks traffic participants, correlates pixel movement with physical road geometry, and outputs structured numerical observations.

```mermaid
sequenceDiagram
    participant Cam as Video Stream / MP4
    participant Ingest as Frame Ingestion (OpenCV)
    participant Det as YOLOv8 Detector
    participant Track as ByteTrack / Centroid
    participant ROI as Lane ROI & Spatial Filter
    participant Feat as Feature Aggregator
    participant State as Traffic State Engine

    loop Every Frame (or every Nth frame)
        Cam->>Ingest: Raw Frame (HxWxC)
        Ingest->>Det: Preprocessed Tensor (640x640)
        Det-->>Track: Detections [x1, y1, x2, y2, conf, cls]
        Track-->>ROI: Tracklets [track_id, bbox, history]
        ROI-->>Feat: Filtered Vehicles inside Road ROI
        Feat->>State: Frame Metrics (Count, Speed, Density, StopTime)
    end
```

## 2. Step-by-Step Processing Stages

### Stage 1: Frame Ingestion & Preprocessing
- Input: RTSP H.264 stream or local MP4 video file.
- Resizing: Scaled to input tensor dimensions ($640 \\times 640$ pixels) maintaining aspect ratio with letterboxing.
- Frame Rate Management: Configurable inference skip rate (e.g., process 1 out of every 2 frames on low-tier i3 hardware to ensure real-time latency).

### Stage 2: Object Detection (YOLOv8)
- Model: Pretrained `yolov8n.pt` (COCO dataset weights).
- Filtered Classes:
  - Class 0: `person`
  - Class 2: `car`
  - Class 3: `motorcycle`
  - Class 5: `bus`
  - Class 7: `truck`
- Confidence Threshold: Default $\\ge 0.35$ to eliminate noise while retaining distant vehicles.
- Non-Maximum Suppression (NMS) IoU Threshold: $0.45$.

### Stage 3: Multi-Object Tracking
- Associating detections across consecutive frames to assign persistent IDs (`track_id`).
- Trajectory History: Maintains a rolling buffer of centroid coordinates $[(x_1, y_1), (x_2, y_2), \\dots, (x_k, y_k)]$ for up to 30 frames.

### Stage 4: ROI Filtering & Perspective Transformation
- Users define an arbitrary polygon representing the drivable road corridor.
- Point-in-Polygon (Ray casting) algorithm tests vehicle centroids:
  $$\\text{inside} = \\text{cv2.pointPolygonTest}(\\text{ROI}, (c_x, c_y), \\text{False}) \\ge 0$$
- Detections outside the drivable road ROI (e.g., parked cars inside a private building compound or pedestrians on elevated footpaths) are excluded from the road state calculation.

### Stage 5: Structured Data Output
Every observation cycle (e.g., every 1.0 second), the pipeline emits a structured JSON payload:
```json
{
  "camera_id": "CAM_01",
  "road_id": "ROAD_JM_01",
  "timestamp": "2026-09-29T19:30:00Z",
  "fps": 22.4,
  "counts": {
    "car": 18,
    "motorcycle": 24,
    "bus": 2,
    "truck": 1,
    "person": 4,
    "total_vehicles": 45
  },
  "metrics": {
    "occupancy_ratio": 0.72,
    "average_speed_kmh": 14.5,
    "stationary_vehicle_count": 12,
    "queue_length_meters": 48.0,
    "queue_persistence_seconds": 38.0
  }
}
```
"""

docs["10_DATASET_AND_ANNOTATION.md"] = """# 10. Dataset and Annotation

## 1. Academic Dataset Strategy
Consistent with SPPU CS-331-FP guidelines and realistic student computing constraints:
1. **Pretrained Baseline:** Use standard COCO weights for initial detection validation.
2. **Targeted Fine-Tuning Dataset:** A curated, project-specific dataset of Indian urban traffic scenes (Pune roads such as Shivajinagar, JM Road, FC Road, Swargate) comprising **300–800 annotated frames** if fine-tuning is required.
3. **Traffic State Classification Dataset:** A collection of **50–100 video clips** (5 to 15 seconds each) capturing specific operational states.

## 2. Annotation Formats & Directory Layout

### 2.1 Object Detection Dataset (YOLO Format)
Each image file has a corresponding `.txt` file with normalized bounding boxes:
`<class_id> <x_center> <y_center> <width> <height>`

```
dataset/
├── detection/
│   ├── data.yaml
│   ├── images/
│   │   ├── train/  # 70% of footage
│   │   ├── val/    # 15% of footage
│   │   └── test/   # 15% of footage
│   └── labels/
│       ├── train/
│       ├── val/
│       └── test/
```

#### `data.yaml` Schema
```yaml
path: ../dataset/detection
train: images/train
val: images/val
test: images/test

names:
  0: person
  1: motorcycle
  2: car
  3: bus
  4: truck
```

### 2.2 Video-Level Splitting Rule (Anti-Leakage)
> [!CRITICAL]
> **Data Leakage Prevention:** In video-based machine learning, adjacent frames in the same video clip are almost identical. Randomly splitting individual frames into train and test sets leads to artificial, fabricated accuracy scores ($>99\%$) that collapse in real life.
> **Rule:** Whole videos must be assigned to either `train`, `val`, or `test`. No frame from Video A may ever appear in the validation or test sets if Video A was used in training.

### 2.3 Traffic State Classification Dataset
A structured CSV dataset linking extracted temporal features to ground-truth traffic states:
```csv
clip_id,camera_id,vehicle_count,avg_speed,occupancy_ratio,stationary_ratio,queue_persistence_s,pedestrian_count,ground_truth_state
clip_001.mp4,CAM_01,42,4.2,0.88,0.76,65.0,2,HEAVY_CONGESTION
clip_002.mp4,CAM_01,12,38.5,0.22,0.00,0.0,0,FREE_FLOW
clip_003.mp4,CAM_02,30,1.5,0.75,0.85,25.0,1,SIGNAL_QUEUE
clip_004.mp4,CAM_03,4,0.0,0.40,1.00,180.0,120,PEDESTRIAN_CROWD
clip_005.mp4,CAM_04,0,0.0,0.00,0.00,0.0,0,BLOCKED
```
"""

for fname, content in docs.items():
    with open(os.path.join(docs_dir, fname), "w", encoding="utf-8") as f:
        f.write(content.strip() + "\\n")

print(f"Generated {len(docs)} documents successfully (Part 1).")
