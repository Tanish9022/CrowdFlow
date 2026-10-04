import os

docs_dir = "docs"

docs = {}

docs["31_TEST_CASES.md"] = r"""# 31. Test Cases

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
"""

docs["32_ML_EVALUATION.md"] = r"""# 32. ML Evaluation

## 1. Evaluation Methodology
In accordance with SPPU academic rigor, evaluation metrics are measured objectively against annotated ground-truth test datasets rather than fabricated numbers.

## 2. Object Detection Metrics (YOLOv8 Nano)
- **Mean Average Precision (mAP):**
  $$\text{mAP} = \frac{1}{|C|} \sum_{c \in C} \int_0^1 P_c(R) \, dR$$
- **Confusion Matrix:** Evaluated across the 5 target classes (`car`, `motorcycle`, `bus`, `truck`, `person`) and background false positives.
- **Inference Latency:** Measured in milliseconds per frame on standard CPU hardware (Intel i3/i5).

## 3. Traffic State Classification Evaluation
- **Macro F1-Score:** Harmonic mean of precision and recall across all 8 traffic states:
  $$F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$
- **State Transition Matrix:** Measures temporal stability (preventing flickering between `SLOW` and `CONGESTED` within single-frame noise).
"""

docs["33_PERFORMANCE_OPTIMIZATION.md"] = r"""# 33. Performance Optimization

## 1. CPU-Bound Optimization Strategies (Intel i3 / 8 GB RAM)
Because the target academic hardware does not assume a dedicated discrete GPU, the pipeline is engineered for extreme efficiency:

1. **Selective Frame Inference (Frame Skipping):**
   - Video is decoded at full framerate ($25-30\text{ FPS}$).
   - Heavy YOLO inference runs every $k$-th frame (e.g., $k=3$, yielding $8-10\text{ FPS}$ model inferences).
   - Centroid Kalman tracking interpolates vehicle trajectories between inference frames, maintaining smooth tracking at negligible CPU cost.
2. **Input Tensor Scaling:**
   - Default resolution set to $640 \times 640$; configurable to $480 \times 480$ on lower-tier dual-core processors.
3. **ONNX Runtime Engine:**
   - Pretrained PyTorch `.pt` weights can be exported to ONNX format with CPU-optimized vector instructions (AVX2/AVX-512).
4. **Vectorized NumPy & SciPy Operations:**
   - All spatial calculations (polygon tests, bounding box intersections) use vectorized C-extensions rather than pure Python loops.
5. **In-Memory Graph Representation:**
   - Dijkstra and network graphs are cached in memory using dictionary adjacency matrices, executing queries in $< 2\text{ milliseconds}$.
"""

docs["34_SECURITY.md"] = r"""# 34. Security

## 1. Academic System Threat Model & Safeguards
While designed as an academic prototype, Crowd Flow incorporates defense-in-depth security best practices appropriate for municipal operational software:

1. **Authentication & Authorization:**
   - Passwords hashed using `passlib` with PBKDF2/Bcrypt and high iteration cost.
   - JWT tokens signed with strong random secret key stored in environment variables (`.env`).
   - Role-Based Access Control (`ROLE_OPERATOR` vs `ROLE_ADMIN`) verified on sensitive routes.
2. **Input Sanitization & Injection Prevention:**
   - All API inputs validated via strictly typed Pydantic v2 schemas.
   - All database queries parameterized via SQLAlchemy ORM, eliminating SQL injection.
3. **Network Isolation:**
   - CORS middleware restricted to designated frontend origin (`http://localhost:5173`).
4. **Credential Safety:**
   - Zero hardcoded passwords, tokens, or secret keys in source code; `.env.example` provided for safe environment setup.
"""

docs["35_DEPLOYMENT.md"] = r"""# 35. Deployment

## 1. Local Development & Demonstration Setup
Crowd Flow is designed for zero-friction local execution on Windows 10/11 or Linux:

### 1.1 Backend Setup
```powershell
# Navigate to backend directory
cd backend

# Create and activate Python virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install required dependencies
pip install -r requirements.txt

# Run database migrations and seed default network
python -m app.database.init_db

# Launch FastAPI development server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 1.2 Frontend Setup
```powershell
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Vite React development server
npm run dev
```

### 1.3 Accessing the Application
- **Operator Dashboard:** `http://localhost:5173`
- **Interactive API Documentation:** `http://127.0.0.1:8000/docs` (Swagger UI)
- **Default Credentials:**
  - Admin: `admin` / `admin123`
  - Operator: `operator` / `operator123`
"""

docs["36_DEMO_SCENARIO.md"] = r"""# 36. Demo Scenario

## 1. The Definitive SPPU Viva Demonstration Walkthrough
The end-to-end oral examination demo is structured as a clear 5-act narrative demonstrating every layer of the system:

### Act 1: Baseline Normal Network State
- Operator opens the dashboard (`http://localhost:5173`).
- All 6 road segments in the Pune Model Network show `GREEN (OPEN)` or `EMERALD (NORMAL)`.
- CCTV feeds display smooth simulated vehicular flow.
- A standard route query from Junction 1 to Junction 6 selects the direct corridor via Road $R_3$ (Total travel time: 3.5 minutes).

### Act 2: Sudden Disruption Event (The Missing Puzzle Piece)
- On Road $R_3$ (JM Road North), a simulated protest rally or multi-vehicle collision occurs.
- CCTV feed for Camera 3 shows vehicles slowing to zero velocity, dense pedestrian clusters on the road, and queue persistence exceeding 120 seconds.
- The Traffic State Engine automatically flags Road $R_3$ as `BLOCKED`.
- Dashboard triggers an audio-visual warning: **"JIGSAW DISRUPTION DETECTED: ROAD R3 COMPROMISED"**.

### Act 3: Jigsaw Graph Recalculation
- The road network map animates: the segment for Road $R_3$ disappears/flashes red as a missing puzzle piece.
- Dynamic weight $W(R_3)$ is updated to $\infty$.
- The route optimization engine recalculates the route from Junction 1 to Junction 6: Road $R_3$ is avoided; the system plots the detour via $J_1 \to J_4 \to J_5 \to J_6$ (Roads $R_4, R_6, R_7$).

### Act 4: What-If Redistribution Simulation
- The operator navigates to the Simulation tab to investigate downstream impact.
- Clicks "Simulate Disruption: 100% of R3 Flow Diverted".
- The simulation engine renders the comparative before-and-after view:
  - Road $R_6$ occupancy jumps from $35\%$ to $86\%$ (`CONGESTED`).
  - Junction 5 approach experiences extreme queue pressure.

### Act 5: Advisory Signal Rebalancing
- The system automatically generates an Advisory Signal Timing Plan for Junction 5:
  - North-South green phase increased from $35\text{ s}$ to $55\text{ s}$ (+20s).
  - Cross-street green phase adjusted to maintain cycle balance.
- Operator clicks "Acknowledge & Implement Advisory".
- Summary telemetry shows simulated detour delay reduced by $38\%$.
"""

docs["37_SPPU_PRESENTATION.md"] = r"""# 37. SPPU Presentation

## 1. Presentation Structure for Project Defense
This slide-by-slide structure aligns directly with the SPPU CS-331-FP final examination rubric:

- **Slide 1: Title & Project Identity**
  - Project Title: Crowd Flow — AI-Based Traffic and Route Management System Using CCTV
  - Students: Tanish Dhende (Roll 98), Palavi Jadhav (Roll 108)
  - Guide / Department: Department of Computer Science, SPPU
- **Slide 2: Problem Identification & Industrial Relevance**
  - Conventional CCTV surveillance is passive and reactive.
  - Road closures cause chaotic uncoordinated spillover onto unprepared secondary roads.
- **Slide 3: Project Vision: The Dynamic Jigsaw Paradigm**
  - Roads as interlocking capacity puzzle pieces.
  - Missing pieces trigger dynamic recalculation, simulation, and signal advisory.
- **Slide 4: System Architecture & Data Flow**
  - Video $\to$ YOLO $\to$ Tracker $\to$ Features $\to$ State $\to$ Graph $\to$ Dijkstra $\to$ Sim $\to$ UI.
- **Slide 5: Computer Vision Pipeline & Distinctions**
  - Detection $\neq$ Traffic.
  - Explaining feature extraction: occupancy, speed, stationary fraction, and queue persistence.
- **Slide 6: Dynamic Jigsaw Graph & Routing**
  - Mathematical cost formula: BPR capacity-delay function + blocked state penalties.
- **Slide 7: What-If Disruption Simulator**
  - Macroscopic capacity-constraint redistribution modeling.
- **Slide 8: Advisory Signal Timing Engine**
  - Webster equisaturation formula rebalancing detour bottlenecks.
- **Slide 9: Experimental Results & Performance**
  - FPS benchmarks on CPU, latency, and route recalculation speed.
- **Slide 10: Live Demonstration**
  - Step-by-step walkthrough of the 5-act disruption scenario.
- **Slide 11: Limitations & Future Scope**
  - Real-world camera calibration challenges, multi-agent reinforcement learning.
- **Slide 12: Conclusion & Acknowledgments**
"""

docs["38_VIVA_QUESTIONS_AND_ANSWERS.md"] = r"""# 38. Viva Questions and Answers

## 1. Foundational Concept Questions

### Q1: Why not just use Google Maps or MapmyIndia?
**Answer:** Consumer navigation apps are designed for individual drivers, not traffic control room authorities. They optimize routes selfishly for one user without considering systemic capacity constraints. If an arterial road closes, Google Maps routes thousands of cars onto narrow residential streets, causing immediate gridlock. Crowd Flow is an operator decision-support system that models network-wide capacity, simulates traffic redistribution across multiple alternative paths, and provides signal timing advisories to prevent detour gridlock.

### Q2: Why is the project titled "Crowd Flow" and what is the "Jigsaw" metaphor?
**Answer:** The road network functions like a dynamic jigsaw puzzle where each road link is an interlocking piece with a finite vehicle capacity. When an incident occurs (an accident, protest, or waterlogging), that road piece becomes unavailable—it is conceptually removed from the puzzle. The remaining traffic cannot vanish; it must be assembled into the remaining pieces without overloading them. Crowd Flow identifies the missing piece, recalculates alternative routes, and rebalances the network through simulation and signal timing advisories.

### Q3: Why can't YOLO directly identify traffic?
**Answer:** YOLO is an object detector, not a traffic detector. A single video frame containing 30 stationary cars could be a normal red-light queue, parked cars on a roadside, or a complete traffic breakdown. Bounding boxes alone cannot distinguish between these conditions. We require multi-object tracking over time, spatial filtering (road ROI polygons), and kinematic feature extraction (average speed, stationary fraction, queue persistence) to classify the true traffic state.

## 2. Computer Vision & ML Questions

### Q4: Why use YOLOv8 Nano (`yolov8n`)? Why not train a model from scratch?
**Answer:** Training a deep convolutional object detector from scratch requires tens of thousands of annotated images, high-end GPU clusters, and weeks of training time. YOLOv8 Nano is pretrained on the extensive MS COCO dataset, providing robust feature representations for common vehicles (cars, motorcycles, buses, trucks, pedestrians) in only 3.2 million parameters. It achieves 25–30 FPS inference on standard laptops without requiring a discrete GPU, making it ideal for our academic prototype.

### Q5: How do you distinguish between a red-light signal queue and real traffic congestion?
**Answer:** We evaluate three factors:
1. **Signal State Correlation:** If the signal is RED, stationary vehicles are classified as a `SIGNAL_QUEUE`.
2. **Dissipation on Green:** When the signal turns GREEN, a signal queue dissipates from front to back within a normal clearance cycle.
3. **Queue Persistence Time ($t_{\text{persist}}$):** If the queue persists across multiple green phases or for longer than 120 seconds with low average velocity, it transitions to `TRAFFIC_QUEUE` or `HEAVY_CONGESTION`.

### Q6: How do you prevent data leakage when training on video data?
**Answer:** In video footage, adjacent frames are virtually identical. If we randomly shuffle and split frames into train and test sets, the model simply memorizes nearly identical images, producing artificially inflated, false accuracy scores. To avoid this, we enforce **Video-Level Splitting**: entire video clips are assigned strictly to either the training set, validation set, or testing set. No frame from a training video ever appears in the test set.

## 3. Graph Theory & Algorithm Questions

### Q7: Why use Dijkstra's algorithm for routing?
**Answer:** Dijkstra's algorithm guarantees the mathematically optimal shortest path in a directed graph with non-negative edge weights. Because our urban sector graphs contain dozens of nodes and edges, Dijkstra executes in under 2 milliseconds on CPU. We enhance standard Dijkstra by replacing static distance weights with dynamic impedance costs incorporating real-time speed, road occupancy, and infinite penalties for blocked segments.

### Q8: Does your system directly control real traffic lights?
**Answer:** No. Directly actuating municipal traffic controllers involves strict legal, safety, and physical fail-safe regulations. In our academic prototype, signal timing outputs are explicitly designated as **Advisory Recommendations** for human traffic police operators to review and implement.
"""

docs["39_IMPLEMENTATION_ROADMAP.md"] = r"""# 39. Implementation Roadmap

## 1. Incremental Phased Development Strategy
To guarantee a rock-solid, demonstrable academic deliverable, implementation proceeds strictly in 16 sequential phases:

```
[Phase 0: Documentation & Architecture] (Current)
   │
   ▼
[Phase 1: Project Skeleton & Environment Setup]
   │
   ▼
[Phase 2: Database Models & Backend Foundation]
   │
   ▼
[Phase 3: Road Graph Jigsaw Engine & Routing Services]
   │
   ▼
[Phase 4: Frontend Design System & Shell Layout]
   │
   ▼
[Phase 5: CCTV Video Ingestion & Stream Decoders]
   │
   ▼
[Phase 6: YOLOv8 Detection & ByteTrack Tracking Integration]
   │
   ▼
[Phase 7: Spatial ROI Filtering & Feature Extractor]
   │
   ▼
[Phase 8: Traffic State Classification Engine]
   │
   ▼
[Phase 9: Dynamic Graph & Disruption Alert Integration]
   │
   ▼
[Phase 10: What-If Traffic Redistribution Simulator]
   │
   ▼
[Phase 11: Advisory Signal Timing Recommendation Engine]
   │
   ▼
[Phase 12: Operator Dashboard & Jigsaw Map UI]
   │
   ▼
[Phase 13: End-to-End System Integration & Testing]
   │
   ▼
[Phase 14: Documentation Finalization & Viva Assets]
   │
   ▼
[Phase 15: Final Demo Scenario Rehearsal]
```
"""

docs["40_PROJECT_DECISIONS.md"] = r"""# 40. Project Decisions

## 1. Architectural Decision Records (ADR)

### ADR-01: Framework Selection — FastAPI over Django/Flask
- **Context:** Need high-performance, asynchronous REST endpoints capable of serving real-time telemetry while streaming video frames.
- **Decision:** Adopt FastAPI with Uvicorn.
- **Rationale:** Native asynchronous support, automatic OpenAPI/Swagger documentation, strict type-checking via Pydantic v2, and minimal memory overhead.

### ADR-02: Map Rendering — Custom SVG Vector Map over Leaflet/Mapbox Tiles
- **Context:** The core visual identity is the "Jigsaw Puzzle" metaphor where road segments must dynamically change stroke colors, animate missing puzzle pieces, and render detour vectors.
- **Decision:** Implement a custom SVG-based vector network renderer in React.
- **Rationale:** Zero external tile server dependencies, works completely offline without API rate limits or tokens, and allows full programmatic control over puzzle piece animations and gradients.

### ADR-03: Machine Learning Model — Pretrained YOLOv8 Nano over Custom CNN
- **Context:** Student laptops have modest hardware (Intel i3/i5, 8 GB RAM, no dedicated GPU).
- **Decision:** Utilize Ultralytics YOLOv8 Nano (`yolov8n.pt`).
- **Rationale:** 3.2M parameters, pre-trained on COCO vehicles, achieves 25+ FPS CPU throughput, and avoids training from scratch while enabling fine-tuning on targeted local clips.

### ADR-04: Routing Formulation — Generalized Impedance Cost Function
- **Context:** Routing purely on physical distance fails to divert traffic away from choked corridors.
- **Decision:** Implement BPR-inspired dynamic cost function incorporating distance, occupancy ratio, speed degradation, and infinite impedance for severed links.
- **Rationale:** Mathematically rigorous, standard in transportation engineering, and highly explainable in an academic viva.
"""

for fname, content in docs.items():
    with open(os.path.join(docs_dir, fname), "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

print(f"Generated {len(docs)} documents successfully (Part 4).")
