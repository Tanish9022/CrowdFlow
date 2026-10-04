# 40. Project Decisions

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


## Key Decision Tree

`mermaid
flowchart TD
    D1{"Map Visualization?"} -- "Puzzle/Jigsaw" --> R1["Rejected: Not production-realistic"]
    D1 -- "Real Digital Map with Leaflet + OSM" --> A1["Accepted: Google Maps-style UX"]

    D2{"Object Detector?"} -- "YOLOv5" --> R2["Rejected: Older architecture"]
    D2 -- "YOLOv8 Nano" --> A2["Accepted: Best speed/accuracy tradeoff"]

    D3{"Database?"} -- "PostgreSQL" --> R3["Rejected: Overkill for demo"]
    D3 -- "SQLite with WAL" --> A3["Accepted: Zero-config, concurrent reads"]

    D4{"Routing Algorithm?"} -- "A* with heuristic" --> R4["Rejected: Heuristic calibration needed"]
    D4 -- "Modified Dijkstra" --> A4["Accepted: Exact shortest path, simple"]
`

