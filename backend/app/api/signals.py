"""
Signal Recommendations API Router for Crowd Flow.
Academic Prototype - SPPU CS-331-FP
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.schemas.signals import SignalRecommendationOut
from app.recommendations.signal_engine import signal_engine
from app.graph.jigsaw_engine import jigsaw_engine

router = APIRouter(prefix="/signals", tags=["Signal Timing Recommendations"])


@router.get("/recommendations", response_model=List[SignalRecommendationOut])
def get_signal_recommendations(db: Session = Depends(get_db)):
    """
    Returns advisory signal timing plans calculated via Webster equisaturation
    to rebalance green phases along active detour corridors.
    """
    recs = signal_engine.generate_recommendations(db, active_disruptions=jigsaw_engine.active_disruptions)
    return recs
