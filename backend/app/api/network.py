"""
Network & Jigsaw Graph API Router for Crowd Flow.
Academic Prototype - SPPU CS-331-FP
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database.session import get_db
from app.models.road import RoadNode, RoadEdge
from app.schemas.network import RoadNodeOut, RoadEdgeOut, RoadStatusUpdate, NetworkGraphOut
from app.graph.jigsaw_engine import jigsaw_engine

router = APIRouter(prefix="/network", tags=["Road Network & Jigsaw Graph"])


@router.get("/graph", response_model=NetworkGraphOut)
def get_full_network_graph(db: Session = Depends(get_db)):
    """Returns the current state of the road network and dynamic jigsaw graph."""
    if len(jigsaw_engine.graph.nodes) == 0:
        jigsaw_engine.load_from_db(db)

    topology = jigsaw_engine.get_topology_dict()
    return topology


@router.get("/roads", response_model=List[RoadEdgeOut])
def list_roads(db: Session = Depends(get_db)):
    """Lists all directional road segments."""
    return db.query(RoadEdge).all()


@router.patch("/roads/{road_id}/status", response_model=RoadEdgeOut)
def update_road_status(road_id: str, update: RoadStatusUpdate, db: Session = Depends(get_db)):
    """
    Manually overrides or AI-updates a road segment status (e.g. BLOCKED, CONGESTED, OPEN).
    Immediately updates the in-memory Jigsaw graph impedance cost.
    """
    road = db.query(RoadEdge).filter(RoadEdge.road_id == road_id).first()
    if not road:
        raise HTTPException(status_code=404, detail=f"Road {road_id} not found.")

    road.current_status = update.status
    db.commit()
    db.refresh(road)

    # Synchronize in-memory jigsaw graph
    jigsaw_engine.update_road_status(road_id, update.status)

    return road
