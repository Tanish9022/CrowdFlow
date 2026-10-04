# 06. Tech Stack and Architecture

## 1. Architectural Philosophy
Crowd Flow follows a **Modular Clean Architecture** pattern designed to separate computer vision perception from higher-level graph algorithms and user interfaces. This decoupling ensures that edge camera failures or model updates do not disrupt graph routing or operator dashboard functionality.

## 2. High-Level Architectural Diagram

```mermaid
graph TD
    subgraph "Perception Layer"
        CAM[CCTV Video Streams / MP4 Feeds] --> DECODE[OpenCV Frame Ingestion]
        DECODE --> DET[YOLOv8 Object Detector]
        DET --> TRACK[ByteTrack / Centroid Tracker]
        TRACK --> ROI[Lane ROI Filter & Spatial Coordinates]
        ROI --> FEAT[Kinematic Feature Extractor]
    end

    subgraph "Intelligence & Decision Layer"
        FEAT --> STATE[Traffic State Classifier]
        STATE --> JIGSAW[Dynamic Internal Road Graph Engine]
        JIGSAW --> ROUTE[Dijkstra Dynamic Route Optimizer]
        JIGSAW --> SIM[What-If Traffic Redistribution Simulator]
        SIM --> SIG[Advisory Signal Timing Engine]
    end

    subgraph "Storage & Communication Layer"
        DB[(SQLite / PostgreSQL Database)]
        STATE <--> DB
        JIGSAW <--> DB
        SIG <--> DB
        API[FastAPI REST API Endpoints]
        STATE --> API
        JIGSAW --> API
        ROUTE --> API
        SIM --> API
        SIG --> API
    end

    subgraph "Presentation Layer (Real Digital Map UI)"
        API <--> DASH[React Command Center Dashboard]
        DASH --> VIZ1[Live CCTV Video Grid & HUD]
        DASH --> VIZ2[Real Digital Vector Map Overlay (Google-Maps-Style)]
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
| **Graph Operations** | Custom Python Engine + NetworkX | Neo4j, pgRouting | In-memory graph operations ensure sub-millisecond route recalculation with BPR dynamic impedance. |
| **Database** | SQLite (dev) / PostgreSQL (prod)| MongoDB, Redis | ACID compliance for relational graph nodes, edges, logs, and zero-configuration portability for academic viva. |
| **Frontend UI** | React 18 + SVG Vector Map | Next.js, Vue, Leaflet | Modular component architecture, direct SVG control for real Google-Maps-like vector road network rendering with live traffic color overlays. |\n