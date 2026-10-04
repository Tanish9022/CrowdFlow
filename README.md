# Crowd Flow
## AI-Based Traffic and Route Management System Using CCTV

> **SPPU T.Y. B.Sc. Computer Science Final Year Project (CS-331-FP)**  
> **Students:**  
> - Tanish Dhende — Roll No. 98  
> - Palavi Jadhav — Roll No. 108  

---

### Core Concept: The Dynamic Jigsaw Road Network
Crowd Flow models an urban traffic network as a **Dynamic Jigsaw Puzzle**. During disruptions (protests, religious processions, road work, waterlogging, or severe collisions), compromised roads become unavailable—becoming missing pieces in the traffic puzzle. Crowd Flow:

1. Ingests CCTV video feeds and detects mobility participants (cars, motorcycles, buses, trucks, pedestrians).
2. Tracks vehicles across frames to extract real-world metrics (speed, occupancy, stationary ratio, queue length, and persistence).
3. Classifies operational traffic states (`FREE_FLOW`, `SLOW`, `SIGNAL_QUEUE`, `HEAVY_CONGESTION`, `PARKED`, `PEDESTRIAN_CROWD`, `BLOCKED`).
4. Represents the road network as a dynamic directed graph with capacity-impedance weights.
5. Treats blocked segments as missing puzzle pieces, automatically recalculating feasible detour routes avoiding saturated links.
6. Simulates traffic redistribution via a transparent macroscopic What-If model.
7. Generates advisory traffic signal timing recommendations to prevent detour gridlock.
8. Displays real-time situational awareness on an operator command dashboard.

---

### System Architecture Pipeline
```
CCTV Perception
  │  (YOLOv8 Detection + ByteTrack / Centroid Tracking)
  ▼
Traffic Feature Extraction
  │  (Velocity, Density, Stationary Duration, Queue Persistence)
  ▼
Traffic-State Engine
  │  (Distinguishes Signal Queues vs Real Congestion vs Parked Cars)
  ▼
Internal Dynamic Road Graph (BPR Impedance Engine)
  │  (Generalized Cost Calculation & Disrupted Link Invalidation)
  ▼
Alternative Detour Routing & What-If Simulation
  │  (Dynamic Dijkstra Paths, Macroscopic Capacity Spillover)
  ▼
Real Digital Road Map Visualization & Advisory Panel
  │  (Google-Maps-Style Vector Map Overlay: 🟢 🟡 🔴 ⚫ 📍 ➡️)
  ▼
Signal Recommendations & Command Dashboard
     (Webster Green Rebalancing, Obsidian TOC Interface)
```

---

### Quick Start Guide

#### Prerequisites
- Python 3.10+ (Tested on 3.12)
- Node.js 18+ (Tested on v22)
- Modern web browser (Chrome, Edge, Firefox)

#### 1. Backend Setup
```bash
cd backend
python -m venv venv

# Windows:
.\venv\Scripts\Activate.ps1
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
API Documentation available at: `http://127.0.0.1:8000/docs`

#### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Dashboard available at: `http://localhost:5173`

---

### Engineering Source of Truth
The canonical system specification is documented in `/docs` across 40 specialized engineering design files:
- [01. Project Vision](docs/01_PROJECT_VISION.md)
- [06. Tech Stack & Architecture](docs/06_TECH_STACK_AND_ARCHITECTURE.md)
- [09. CCTV AI Pipeline](docs/09_CCTV_AI_PIPELINE.md)
- [13. Traffic State Engine](docs/13_TRAFFIC_STATE_ENGINE.md)
- [15. Road Graph Jigsaw Engine](docs/15_ROAD_GRAPH_JIGSAW_ENGINE.md)
- [17. Traffic Simulation](docs/17_TRAFFIC_SIMULATION.md)
- [18. Signal Recommendation](docs/18_SIGNAL_RECOMMENDATION.md)
- [36. Demo Scenario](docs/36_DEMO_SCENARIO.md)
- [38. Viva Questions & Answers](docs/38_VIVA_QUESTIONS_AND_ANSWERS.md)

