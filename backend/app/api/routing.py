"""
Route Optimization API Router for Crowd Flow.
Academic Prototype - SPPU CS-331-FP
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.routing import RouteRequest, RouteResponse
from app.routing.dijkstra import route_optimizer
from app.graph.jigsaw_engine import jigsaw_engine

router = APIRouter(prefix="/routing", tags=["Routing & Detours"])


@router.post("/calculate", response_model=RouteResponse)
def calculate_optimal_route(req: RouteRequest, db: Session = Depends(get_db)):
    """
    Calculates primary optimal route and K-shortest detour alternatives
    using dynamic BPR generalized impedance costs while avoiding missing/blocked pieces.
    """
    if len(jigsaw_engine.graph.nodes) == 0:
        jigsaw_engine.load_from_db(db)

    result = route_optimizer.find_routes(
        source_node_id=req.source_node_id,
        target_node_id=req.target_node_id,
        avoid_blocked=req.avoid_blocked,
        k_alternatives=3 if req.calculate_alternatives else 0
    )

    return result
