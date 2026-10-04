"""
What-If Redistribution Simulation API Router for Crowd Flow.
Academic Prototype - SPPU CS-331-FP
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.simulation import SimulationRequest, SimulationResponse
from app.simulation.redistributor import simulator
from app.graph.jigsaw_engine import jigsaw_engine

router = APIRouter(prefix="/simulation", tags=["What-If Simulation"])


@router.post("/run", response_model=SimulationResponse)
def run_whatif_simulation(req: SimulationRequest, db: Session = Depends(get_db)):
    """
    Executes a macroscopic traffic redistribution simulation for a disabled road link.
    Returns comparative before vs. after telemetry and overloaded corridor flags.
    """
    if len(jigsaw_engine.graph.nodes) == 0:
        jigsaw_engine.load_from_db(db)

    try:
        report = simulator.simulate_disruption(
            blocked_road_id=req.blocked_road_id,
            disruption_type=req.disruption_type,
            custom_volume_vph=req.diverted_volume_vph,
            theta=req.dispersion_theta
        )
        return report
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {e}")
