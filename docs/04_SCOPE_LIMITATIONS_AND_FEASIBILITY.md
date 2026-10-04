# 04. Scope, Limitations, and Feasibility

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
- Every mathematical step (graph cost, queue formula, green split advisory) is transparent and explainable to examiners.\n


## Scope Boundary Diagram

`mermaid
flowchart LR
    subgraph "In Scope"
        A1["CCTV video analysis"]
        A2["Vehicle detection + tracking"]
        A3["Traffic state classification"]
        A4["Dynamic road graph"]
        A5["Route optimization"]
        A6["What-If simulation"]
        A7["Signal advisory"]
    end

    subgraph "Out of Scope"
        B1["Hardware signal actuation"]
        B2["City-wide deployment"]
        B3["GPS-based vehicle tracking"]
        B4["Cloud infrastructure"]
        B5["Mobile app for drivers"]
    end
`

