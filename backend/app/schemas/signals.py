from pydantic import BaseModel
from typing import Dict, Any, Optional, List


class SignalPlanSchema(BaseModel):
    junction_id: str
    junction_name: str
    cycle_time_seconds: int
    current_plan: Dict[str, int]
    active_phase: str
    time_remaining_seconds: int


class SignalRecommendationOut(BaseModel):
    id: int
    signal_id: str
    junction_name: str
    current_timings: Dict[str, int]
    recommended_timings: Dict[str, int]
    justification: str
    expected_delay_reduction_pct: int
    is_accepted: bool
    recommended_at: str
