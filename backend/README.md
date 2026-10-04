# Backend Service — Crowd Flow

## Overview
FastAPI backend service providing:
- Asynchronous RESTful APIs and WebSocket telemetry.
- Computer vision ingestion (OpenCV + YOLOv8 + ByteTrack).
- Traffic state classification engine.
- Dynamic Jigsaw Graph network & modified Dijkstra routing.
- Macroscopic What-If traffic redistribution simulation.
- Advisory traffic signal timing recommendation.
- Relational database persistence with SQLAlchemy.

## Running Locally
```bash
# In backend directory
python -m venv venv
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python -m app.main
```
Server runs at `http://127.0.0.1:8000`. API Docs available at `http://127.0.0.1:8000/docs`.
