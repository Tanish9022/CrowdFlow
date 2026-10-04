# System Architecture

## Architecture Overview
Crowd Flow adopts a Decoupled Service-Oriented Architecture (SOA) structured into five core subsystems:

```
[ CCTV Video Feeds / MP4 Clips ]
               │
               ▼
[ Subsystem 1: Computer Vision & Tracking Engine (OpenCV + YOLOv8 + ByteTrack) ]
               │  Structured Observations (Counts, Speeds, Density, Stationary Duration)
               ▼
[ Subsystem 2: Traffic State & Disruption Engine (Rules + Random Forest) ]
               │  Edge States (FREE_FLOW, SLOW, SIGNAL_QUEUE, HEAVY_CONGESTION, BLOCKED)
               ▼
[ Subsystem 3: Dynamic Jigsaw Graph Engine (NetworkX + Impedance Formulation) ]
        ├──► [ Subsystem 4A: Route Optimizer (Dijkstra + Multi-Path Detour) ]
        ├──► [ Subsystem 4B: What-If Redistribution Simulator (Logit Capacity Model) ]
        └──► [ Subsystem 4C: Advisory Signal Split Engine (Webster Equisaturation) ]
               │
               ▼
[ Subsystem 5: Presentation & Telemetry Layer (FastAPI REST/WebSocket + React Dashboard) ]
```

## Directory Structure
- `/architecture`: High-level system diagrams, component boundaries, and pipeline specifications.
- `/docs`: The 40 canonical Markdown documentation source-of-truth files.
- `/backend`: Python FastAPI application backend.
- `/frontend`: React + Vite operator command dashboard.
- `/dataset`: Data placeholders, annotation schemas, and sample clips.
- `/training`: Reproducible training and validation scripts for YOLO and classifier.
- `/models`: Weight storage directory (Git-ignored binary weights; placeholder README only).
- `/tests`: Unit, integration, and scenario-based test suites.
- `/scripts`: Utility tools, mock stream generators, and database seeding scripts.
