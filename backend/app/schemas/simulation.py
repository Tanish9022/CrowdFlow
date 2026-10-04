from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class SimulationRequest(BaseModel):
    blocked_road_id: str
    disruption_type: str = Field(default="PROTEST", description="PROTEST, ACCIDENT, ROAD_CLOSURE, WATERLOGGING")
    diverted_volume_vph: Optional[float] = Field(default=None, description="Displaced flow; defaults to current road volume")
    dispersion_theta: float = Field(default=0.005, description="Logit choice sensitivity coefficient")


class SimulatedEdgeDelta(BaseModel):
    road_id: str
    road_name: str
    baseline_volume_vph: float
    simulated_volume_vph: float
    volume_delta_vph: float
    capacity_vph: int
    baseline_occupancy: float
    simulated_occupancy: float
    status_before: str
    status_after: str
    is_overloaded: bool  # occupancy > 0.85
    baseline_speed_kmh: float
    simulated_speed_kmh: float


class SimulationResponse(BaseModel):
    scenario_id: str
    disruption_type: str
    blocked_road_id: str
    blocked_road_name: str
    displaced_volume_vph: float
    total_affected_roads: int
    overloaded_roads_count: int
    network_average_delay_increase_pct: float
    affected_edges: List[SimulatedEdgeDelta]
    recommended_detour_path: List[str]
