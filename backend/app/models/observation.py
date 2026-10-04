from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.base import Base


class TrafficObservation(Base):
    __tablename__ = "traffic_observations"

    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=False)
    road_id = Column(Integer, ForeignKey("road_edges.id"), nullable=False)
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    
    # Kinematic & Count Metrics
    vehicle_count = Column(Integer, default=0)
    pedestrian_count = Column(Integer, default=0)
    class_breakdown = Column(JSON, nullable=True) # {"car": 12, "motorcycle": 8, "bus": 2, "truck": 1}
    average_speed_kmh = Column(Float, default=0.0)
    occupancy_ratio = Column(Float, default=0.0)
    stationary_vehicle_count = Column(Integer, default=0)
    queue_length_meters = Column(Float, default=0.0)
    queue_persistence_seconds = Column(Float, default=0.0)
    
    # Classification Results
    traffic_state = Column(String(50), default="NORMAL", index=True) # FREE_FLOW, SLOW, SIGNAL_QUEUE, HEAVY_CONGESTION, etc.
    road_status = Column(String(30), default="OPEN") # OPEN, SLOW, CONGESTED, BLOCKED

    # Relationships
    camera = relationship("Camera", back_populates="observations")
    road = relationship("RoadEdge", back_populates="observations")
