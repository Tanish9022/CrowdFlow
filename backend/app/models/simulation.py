from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime, timezone
from app.database.base import Base


class SimulationRun(Base):
    __tablename__ = "simulation_runs"

    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(String(50), unique=True, index=True, nullable=False)
    disruption_type = Column(String(50), nullable=False) # PROTEST, ACCIDENT, ROAD_CLOSURE, WATERLOGGING
    blocked_road_id = Column(String(50), nullable=False)
    diverted_volume_vph = Column(Float, nullable=False)
    executed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    
    # JSON payload of comparison metrics before vs. simulated after
    summary_metrics = Column(JSON, nullable=False)
    affected_edges = Column(JSON, nullable=False)
