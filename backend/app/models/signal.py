from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.base import Base


class TrafficSignal(Base):
    __tablename__ = "traffic_signals"

    id = Column(Integer, primary_key=True, index=True)
    signal_id = Column(String(50), unique=True, index=True, nullable=False)
    junction_node_id = Column(Integer, ForeignKey("road_nodes.id"), nullable=False)
    junction_name = Column(String(100), nullable=False)
    
    cycle_time_seconds = Column(Integer, default=90)
    current_plan = Column(JSON, nullable=False) # {"NS_green": 40, "EW_green": 40, "yellow": 5, "all_red": 5}
    active_phase = Column(String(50), default="PHASE_NS_GREEN")
    time_remaining_seconds = Column(Integer, default=25)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    junction_node = relationship("RoadNode", back_populates="signals")
    recommendations = relationship("SignalRecommendation", back_populates="signal")


class SignalRecommendation(Base):
    __tablename__ = "signal_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    signal_id = Column(Integer, ForeignKey("traffic_signals.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    
    current_timings = Column(JSON, nullable=False)
    recommended_timings = Column(JSON, nullable=False) # {"NS_green": 55, "EW_green": 25}
    justification = Column(String(255), nullable=False)
    expected_delay_reduction_pct = Column(Integer, default=25)
    
    is_accepted = Column(Boolean, default=False)
    reviewed_at = Column(DateTime, nullable=True)

    # Relationships
    signal = relationship("TrafficSignal", back_populates="recommendations")
