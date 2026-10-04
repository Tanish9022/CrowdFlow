import os
from pathlib import Path
from typing import List
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_DB_PATH = BASE_DIR / "crowd_flow.db"


class Settings(BaseModel):
    APP_NAME: str = "Crowd Flow — AI-Based Traffic & Route Management"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "crowd_flow_secret_key_sppu_cs331fp_2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # Database: Absolute path prevents relative CWD discrepancies
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH.as_posix()}")

    # CCTV & Computer Vision Defaults
    YOLO_MODEL_PATH: str = os.getenv("YOLO_MODEL_PATH", "yolov8n.pt")
    CONFIDENCE_THRESHOLD: float = 0.35
    IOU_THRESHOLD: float = 0.45
    FRAME_SKIP_RATE: int = 2

    # Graph & BPR Cost Parameters
    BPR_ALPHA: float = 0.15
    BPR_BETA: float = 4.0
    MIN_SPEED_KMH: float = 2.0
    BLOCKED_PENALTY: float = 1e9

    # Signal Defaults
    DEFAULT_CYCLE_TIME_SECONDS: int = 90
    MIN_GREEN_SECONDS: int = 15
    MAX_GREEN_SECONDS: int = 70

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]


settings = Settings()
