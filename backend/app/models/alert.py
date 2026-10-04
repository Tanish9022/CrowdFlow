from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.base import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    road_id = Column(Integer, ForeignKey("road_edges.id"), nullable=False)
    alert_type = Column(String(50), nullable=False) # BLOCKED_ROAD, HEAVY_CONGESTION, PEDESTRIAN_CROWD
    severity = Column(String(20), default="WARNING") # INFO, WARNING, CRITICAL
    message = Column(String(255), nullable=False)
    triggered_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    
    is_acknowledged = Column(Boolean, default=False, index=True)
    acknowledged_by = Column(String(50), nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)

    # Relationships
    road = relationship("RoadEdge", back_populates="alerts")
