from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="ROLE_OPERATOR", nullable=False)  # ROLE_OPERATOR, ROLE_ADMIN
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
