# 05. System Requirements

## 1. Hardware Requirements

### Minimum Requirements (Target Demonstration Laptop)
- **Processor:** Intel Core i3 (7th Gen or newer) or AMD Ryzen 3
- **Clock Speed:** 2.0 GHz or higher (Dual-Core with Hyperthreading)
- **RAM:** 8 GB DDR4
- **Storage:** 10 GB available SSD/HDD storage (for dataset clips, Python virtual environment, dependencies)
- **Display Resolution:** $1366 \times 768$ pixels
- **Input:** Standard Keyboard, Mouse / Trackpad

### Recommended Requirements (Optimal Performance)
- **Processor:** Intel Core i5 / i7 (10th Gen or newer) or AMD Ryzen 5 / 7
- **RAM:** 16 GB DDR4/DDR5
- **GPU (Optional):** NVIDIA GeForce GTX 1650 / RTX 3050 (4 GB VRAM) with CUDA support
- **Display Resolution:** $1920 \times 1080$ Full HD
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
- `fastapi` $\ge 0.110.0$ (High performance ASGI Web API framework)
- `uvicorn[standard]` $\ge 0.28.0$ (ASGI web server)
- `ultralytics` $\ge 8.1.0$ (YOLOv8 object detection)
- `opencv-python-headless` $\ge 4.9.0$ (Computer vision and video frame processing)
- `numpy` $\ge 1.26.0$ (Vectorized array calculations)
- `scipy` $\ge 1.12.0$ (Spatial calculations, Hungarian algorithm)
- `networkx` $\ge 3.2.0$ (Graph modeling and shortest path verification)
- `sqlalchemy` $\ge 2.0.0$ (ORM for relational database management)
- `pydantic` $\ge 2.6.0$ (Data validation and API schemas)
- `python-jose[cryptography]` $\ge 3.3.0$ (JWT token authentication)
- `passlib[bcrypt]` $\ge 1.7.4$ (Password hashing)

#### Frontend & UI
- `react` $\ge 18.2.0$
- `react-dom` $\ge 18.2.0$
- `react-router-dom` $\ge 6.22.0$
- `lucide-react` (Clean engineering iconography)
- `recharts` $\ge 2.12.0$ (Data analytics and telemetry charts)
- Modern Vanilla CSS with CSS Custom Properties (Theme Design System)

## 3. Network Requirements
- Fully self-contained offline capability: System runs entirely on `localhost` (`127.0.0.1:8000` for backend, `127.0.0.1:5173` or `3000` for frontend).
- No continuous external internet connection required during examination viva.\n


## System Requirements Architecture

`mermaid
flowchart TD
    subgraph "Hardware Requirements"
        H1["Intel Core i3+ CPU"]
        H2["8 GB RAM minimum"]
        H3["CCTV Camera feeds"]
    end

    subgraph "Software Requirements"
        S1["Python 3.10+ with FastAPI"]
        S2["Node.js 18+ with React"]
        S3["SQLite with WAL mode"]
        S4["YOLOv8 Nano model"]
    end

    subgraph "Network Requirements"
        N1["RTSP camera streams"]
        N2["localhost REST API"]
        N3["WebSocket telemetry"]
    end

    H1 --> S1
    H2 --> S4
    H3 --> N1
    S1 --> N2
    S2 --> N3
`

