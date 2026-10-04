from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class CameraOut(BaseModel):
    id: int
    camera_id: str
    name: str
    stream_url: str
    monitored_road_id: Optional[int] = None
    monitored_road_name: Optional[str] = None
    status: str
    fps: float
    roi_polygon: Optional[List[List[float]]] = None

    class Config:
        from_attributes = True


class CameraTelemetry(BaseModel):
    camera_id: str
    road_id: str
    road_name: str
    fps: float
    status: str
    vehicle_count: int
    pedestrian_count: int
    class_breakdown: Dict[str, int]
    average_speed_kmh: float
    occupancy_ratio: float
    stationary_count: int
    queue_length_meters: float
    queue_persistence_seconds: float
    traffic_state: str
    road_status: str
    recorded_at: str
