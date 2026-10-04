# 21. Backend Implementation

## 1. Backend Architecture & Package Structure
The backend is structured as a modular FastAPI enterprise application following Domain-Driven Design (DDD) principles:

```
backend/
├── app/
│   ├── main.py              # Application entrypoint & lifespan hooks
│   ├── core/
│   │   ├── config.py        # Settings management via pydantic-settings (.env)
│   │   ├── security.py      # JWT creation, bcrypt password hashing
│   │   └── events.py        # Startup/shutdown hooks
│   ├── database/
│   │   ├── session.py       # SQLAlchemy engine & sessionmaker
│   │   └── base.py          # Declarative Base metadata
│   ├── models/              # SQLAlchemy ORM models (User, Road, Camera, etc.)
│   ├── schemas/             # Pydantic v2 validation models for DTOs
│   ├── api/                 # Versioned REST routers (/v1/network, /v1/cameras, etc.)
│   ├── services/            # Business orchestration services
│   ├── cv/                  # Video ingestion, YOLOv8 detector, ROI polygon tester
│   ├── tracking/            # Multi-object tracking (ByteTrack / Centroid Kalman)
│   ├── traffic/             # Feature aggregation, rule & RF state engine
│   ├── graph/               # NetworkX graph manager, dynamic cost calculation
│   ├── routing/             # Modified Dijkstra & alternative detour solver
│   ├── simulation/          # Macroscopic What-If redistribution engine
│   ├── recommendations/     # Webster advisory signal split engine
│   └── utils/               # Coordinate math, logging helpers, formatting
```

## 2. Concurrency & Async Processing Model
- **Web Requests:** Handled asynchronously via `async def` endpoints on the Uvicorn ASGI event loop.
- **Computer Vision Inference:** Video decoding and YOLO tensor calculations run in dedicated background worker threads or sub-processes (`asyncio.to_thread` / `concurrent.futures.ThreadPoolExecutor`) to prevent blocking API request handling.
- **In-Memory Cache:** Current dynamic graph weights and active camera states are cached in thread-safe in-memory singletons, with asynchronous periodic persistence to the relational database.


## 3. Backend Request Processing Architecture

`mermaid
flowchart TD
    A["HTTP Request"] --> B["Uvicorn ASGI Server"]
    B --> C["FastAPI Middleware"]
    C --> D{"Auth Required?"}
    D -- Yes --> E["JWT Verification"]
    D -- No --> F["Health Check / Public"]
    E --> G["Route to API Endpoint"]
    F --> G
    G --> H{"Endpoint Type"}
    H -- "Graph/Network" --> I["Jigsaw Graph Engine - In Memory"]
    H -- "CRUD" --> J["SQLAlchemy ORM - Database"]
    H -- "CV Stream" --> K["Background Thread Pool"]
    H -- "Simulation" --> L["Redistribution Engine"]
    I --> M["JSON Response"]
    J --> M
    K --> N["MJPEG StreamingResponse"]
    L --> M
    M --> O["Client"]
    N --> O
`

