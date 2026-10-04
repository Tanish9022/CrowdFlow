from pydantic import BaseModel
from typing import List, Optional


class RouteRequest(BaseModel):
    source_node_id: str
    target_node_id: str
    avoid_blocked: bool = True
    calculate_alternatives: bool = True


class PathSegment(BaseModel):
    from_node: str
    to_node: str
    road_id: str
    road_name: str
    status: str
    distance_meters: float
    estimated_time_seconds: float
    cost: float


class RouteOption(BaseModel):
    route_name: str
    nodes: List[str]
    roads: List[str]
    segments: List[PathSegment]
    total_distance_meters: float
    total_time_seconds: float
    total_cost: float
    is_primary: bool
    is_detour: bool


class RouteResponse(BaseModel):
    found: bool
    source_node: str
    target_node: str
    primary_route: Optional[RouteOption] = None
    alternative_routes: List[RouteOption] = []
    message: Optional[str] = None
