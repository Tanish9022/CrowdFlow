from pydantic import BaseModel, Field
from typing import List, Optional


class RoadNodeBase(BaseModel):
    node_id: str
    name: str
    x: float
    y: float
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    node_type: str = "INTERSECTION"


class RoadNodeOut(RoadNodeBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True


class RoadEdgeBase(BaseModel):
    road_id: str
    name: str
    source_node_id: Optional[int] = None
    target_node_id: Optional[int] = None
    source: Optional[str] = None
    target: Optional[str] = None
    length_meters: float = 500.0
    lanes: int = 2
    capacity_vph: int = 1200
    free_flow_speed: float = 50.0
    current_status: str = "OPEN"
    current_vehicle_count: int = 0
    current_average_speed: float = 45.0
    current_occupancy: float = 0.1
    current_dynamic_cost: float = 500.0


class RoadEdgeOut(RoadEdgeBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True


class RoadStatusUpdate(BaseModel):
    status: str = Field(..., description="OPEN, SLOW, CONGESTED, BLOCKED, PARTIALLY_BLOCKED")
    reason: Optional[str] = None


class NetworkGraphOut(BaseModel):
    nodes: List[RoadNodeOut]
    edges: List[RoadEdgeOut]
    active_disruptions: List[str]
    total_capacity_vph: int
    average_network_occupancy: float
