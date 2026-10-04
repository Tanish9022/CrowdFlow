from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.base import Base


class RoadNode(Base):
    __tablename__ = "road_nodes"

    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    x = Column(Float, nullable=False)  # Grid or display coordinate X
    y = Column(Float, nullable=False)  # Grid or display coordinate Y
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    node_type = Column(String(30), default="INTERSECTION")  # INTERSECTION, ROUNDABOUT, HIGHWAY_MERGE

    # Relationships
    outgoing_roads = relationship("RoadEdge", foreign_keys="RoadEdge.source_node_id", back_populates="source_node")
    incoming_roads = relationship("RoadEdge", foreign_keys="RoadEdge.target_node_id", back_populates="target_node")
    signals = relationship("TrafficSignal", back_populates="junction_node")


class RoadEdge(Base):
    __tablename__ = "road_edges"

    id = Column(Integer, primary_key=True, index=True)
    road_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(150), nullable=False)
    source_node_id = Column(Integer, ForeignKey("road_nodes.id"), nullable=False)
    target_node_id = Column(Integer, ForeignKey("road_nodes.id"), nullable=False)
    
    length_meters = Column(Float, nullable=False, default=500.0)
    lanes = Column(Integer, nullable=False, default=2)
    capacity_vph = Column(Integer, nullable=False, default=1200)  # Vehicles per hour
    free_flow_speed = Column(Float, nullable=False, default=50.0) # km/h
    
    # Real-time state
    current_status = Column(String(30), default="OPEN", index=True) # OPEN, SLOW, CONGESTED, BLOCKED, PARTIALLY_BLOCKED
    current_vehicle_count = Column(Integer, default=0)
    current_average_speed = Column(Float, default=45.0)
    current_occupancy = Column(Float, default=0.1)
    current_dynamic_cost = Column(Float, default=500.0)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    source_node = relationship("RoadNode", foreign_keys=[source_node_id], back_populates="outgoing_roads")
    target_node = relationship("RoadNode", foreign_keys=[target_node_id], back_populates="incoming_roads")
    cameras = relationship("Camera", back_populates="monitored_road")
    observations = relationship("TrafficObservation", back_populates="road")
    alerts = relationship("Alert", back_populates="road")
