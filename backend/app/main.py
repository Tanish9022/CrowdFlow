"""
Crowd Flow — AI-Based Traffic and Route Management System Using CCTV
Main FastAPI Application Entrypoint
Academic Prototype - SPPU CS-331-FP
"""

import os
import sys
from pathlib import Path

# Ensure backend directory is in sys.path when launched from root
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.session import engine, SessionLocal
from app.database.base import Base
from app.graph.jigsaw_engine import jigsaw_engine
from app.api import auth, network, routing, simulation, signals, cameras


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure tables exist and load Jigsaw graph into memory
    print(f"=== Starting {settings.APP_NAME} v{settings.APP_VERSION} ===")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        jigsaw_engine.load_from_db(db)
        print(f"[OK] Dynamic Jigsaw Graph loaded: {len(jigsaw_engine.graph.nodes)} nodes, {len(jigsaw_engine.graph.edges)} edges.")
    finally:
        db.close()
    yield
    print("=== Shutting down Crowd Flow backend ===")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="SPPU Final Year B.Sc. Project CS-331-FP | Tanish Dhende & Palavi Jadhav",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permissive for local academic demonstration
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(network.router, prefix=settings.API_V1_PREFIX)
app.include_router(routing.router, prefix=settings.API_V1_PREFIX)
app.include_router(simulation.router, prefix=settings.API_V1_PREFIX)
app.include_router(signals.router, prefix=settings.API_V1_PREFIX)
app.include_router(cameras.router, prefix=settings.API_V1_PREFIX)


@app.get(f"{settings.API_V1_PREFIX}/health", tags=["Health"])
def healthcheck():
    return {
        "status": "HEALTHY",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "active_disruptions": jigsaw_engine.active_disruptions,
        "graph_nodes": len(jigsaw_engine.graph.nodes),
        "graph_edges": len(jigsaw_engine.graph.edges)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
