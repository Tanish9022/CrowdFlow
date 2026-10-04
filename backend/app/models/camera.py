from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.base import Base


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    stream_url = Column(String(255), nullable=False)  # MP4 path, RTSP url, or 'synthetic'
    monitored_road_id = Column(Integer, ForeignKey("road_edges.id"), nullable=True)
    
    status = Column(String(20), default="ONLINE")  # ONLINE, OFFLINE, DEGRADED
    fps = Column(Float, default=25.0)
    roi_polygon = Column(JSON, nullable=True)  # List of [x, y] coordinates for road polygon
    parking_polygon = Column(JSON, nullable=True) # Curbside parking zone polygon
    
    # Relationships
    monitored_road = relationship("RoadEdge", back_populates="cameras")
    observations = relationship("TrafficObservation", back_populates="camera")
