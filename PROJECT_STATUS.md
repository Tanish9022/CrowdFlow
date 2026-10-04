# Project Status — Crowd Flow

**Last Updated:** 2026-09-29  
**Academic Program:** SPPU T.Y. B.Sc. Computer Science (CS-331-FP)  
**Authors:** Tanish Dhende (Roll 98) & Palavi Jadhav (Roll 108)  

---

## 1. Executive Status Summary
- **Current State:** Fully Operational End-to-End Academic Prototype.
- **Architectural Principle:** CCTV Perception $\to$ YOLOv8 & Tracking $\to$ Traffic Density $\to$ Internal Dynamic Road Graph $\to$ Dijkstra Route Optimizer $\to$ Real Digital Map Visualization.
- **Backend:** FastAPI service running with SQLite database (`crowd_flow.db`), NetworkX dynamic impedance graph, modified Dijkstra routing, What-If macroscopic redistribution simulation, and Webster signal advisory engine.
- **Frontend:** React 18 + Vite production build (`dist/`) with Obsidian Command Center dark theme, Google-Maps-style real vector road network map with live traffic flow color overlays (🟢 🟡 🔴 ⚫ 📍 ➡️), multi-stream CCTV grid, What-If simulation workbench, Route optimizer, and Signal Advisory panel.
- **Verification:** All 5 API integration test suites passed (`tests/test_api_endpoints.py`), and the 5-Act Viva demonstration script (`scripts/run_demo_scenario.py`) executed with 100% success.

---

## 2. Component Implementation Status

| Component | Status | Source Location | Test / Verification |
| :--- | :---: | :--- | :--- |
| **Documentation Suite (40 MDs)** | ✅ Completed | `/docs/*` | 40 canonical design files established |
| **Database Schema & Models** | ✅ Completed | `backend/app/models/*` | SQLite seeded with Pune Urban Model Network |
| **Internal Road Graph Engine** | ✅ Completed | `backend/app/graph/jigsaw_engine.py` | BPR dynamic impedance & disrupted link cost calculation |
| **Dynamic Dijkstra Routing** | ✅ Completed | `backend/app/routing/dijkstra.py` | Avoids blocked links; computes K detours |
| **What-If Redistribution Sim** | ✅ Completed | `backend/app/simulation/redistributor.py` | Logit discrete-choice capacity model |
| **Advisory Signal Engine** | ✅ Completed | `backend/app/recommendations/signal_engine.py` | Webster equisaturation green split recalculation |
| **YOLOv8 & Tracking Pipeline** | ✅ Completed | `backend/app/cv/*` | Object detector, Centroid tracker, ROI filter |
| **Traffic State Engine** | ✅ Completed | `backend/app/traffic/state_engine.py` | 8 traffic states; vehicle detection $\neq$ traffic |
| **REST & Streaming Endpoints** | ✅ Completed | `backend/app/api/*` | Network, Routing, Simulation, Signals, Cameras |
| **Obsidian UI & Real Vector Map** | ✅ Completed | `frontend/src/*` | React 18 production bundle with Google-Maps-style vector map |
| **5-Act Viva Demo Script** | ✅ Completed | `scripts/run_demo_scenario.py` | Step-by-step oral presentation rehearsal |
| **Integration Test Suite** | ✅ Completed | `tests/test_api_endpoints.py` | Verified all 5 core subsystems |

---

## 3. How to Run the Prototype Locally

### Backend Server (FastAPI)
```powershell
# From project root
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
- API Documentation (Swagger): `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/api/v1/health`

### Frontend Command Dashboard (React / Vite)
```powershell
# In a separate terminal
cd frontend
npm run dev
```
- Operator Dashboard: `http://localhost:5173`

### Run 5-Act Examination Demo
```powershell
python scripts/run_demo_scenario.py
```

### Run Automated Integration Tests
```powershell
python tests/test_api_endpoints.py
```
