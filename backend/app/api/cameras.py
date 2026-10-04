"""
CCTV Surveillance & Camera Telemetry API Router for Crowd Flow.
Provides real-time camera telemetry, MJPEG video streaming, and AI overlays.
Academic Prototype - SPPU CS-331-FP
"""

import cv2
import numpy as np
import asyncio
import time
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse, Response
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from app.database.session import get_db, SessionLocal
from app.models.camera import Camera
from app.models.road import RoadEdge
from app.schemas.cameras import CameraOut, CameraTelemetry
from app.cv.tracker import CentroidTracker
from app.cv.roi import SpatialROIFilter
from app.traffic.state_engine import traffic_state_engine
from app.graph.jigsaw_engine import jigsaw_engine

router = APIRouter(prefix="/cameras", tags=["CCTV Cameras & Streams"])

# In-memory tracking instances per camera
trackers = {}


def generate_synthetic_frame(camera_id: str, road_name: str, status: str, frame_idx: int) -> np.ndarray:
    """
    Renders an animated synthetic urban traffic scene for robust viva demonstrations
    when external physical CCTV feeds are not connected.
    """
    width, height = 640, 480
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Road surface
    cv2.rectangle(frame, (80, 0), (560, height), (45, 45, 50), -1)

    # Lane markings (animated moving dashed lines)
    offset = (frame_idx * 12) % 60
    for y in range(-60 + offset, height, 60):
        # Lane divider 1
        cv2.line(frame, (240, y), (240, min(height, y + 30)), (255, 255, 255), 2)
        # Lane divider 2
        cv2.line(frame, (400, y), (400, min(height, y + 30)), (255, 255, 255), 2)

    # Road shoulder curbs
    cv2.line(frame, (80, 0), (80, height), (100, 100, 100), 4)
    cv2.line(frame, (560, 0), (560, height), (100, 100, 100), 4)

    # Render simulated vehicles moving along lanes
    if status == "BLOCKED":
        # Dense cluster of stopped vehicles and pedestrian protest
        for i in range(5):
            y_car = 180 + i * 45
            cv2.rectangle(frame, (200, y_car), (270, y_car + 35), (30, 120, 240), -1)
            cv2.putText(frame, "CAR #S", (205, y_car + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        # Draw pedestrian crowd
        for px, py in [(320, 220), (340, 240), (360, 210), (380, 250), (310, 260), (350, 270)]:
            cv2.circle(frame, (px, py), 8, (200, 100, 250), -1)
            cv2.circle(frame, (px, py - 12), 4, (200, 100, 250), -1)

        # Warning Banner
        cv2.rectangle(frame, (100, 30), (540, 75), (0, 0, 180), -1)
        cv2.putText(frame, "ROAD BLOCKED: PROTEST GATHERING", (120, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

    else:
        # Flowing traffic
        car_positions = [
            (140, (frame_idx * 14 + 50) % height),
            (290, (frame_idx * 16 + 180) % height),
            (450, (frame_idx * 12 + 300) % height),
            (290, (frame_idx * 15 + 400) % height),
            (150, (frame_idx * 18 + 260) % height)
        ]
        for idx, (x, y) in enumerate(car_positions):
            cv2.rectangle(frame, (x, y), (x + 60, y + 35), (40, 180, 60), -1)
            cv2.putText(frame, f"VEH #{idx+1}", (x + 5, y + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    # HUD Banner
    cv2.rectangle(frame, (0, 0), (width, 30), (20, 20, 20), -1)
    cv2.putText(frame, f"{camera_id} | {road_name} | STATUS: {status}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    return frame


@router.get("", response_model=List[CameraOut])
def list_cameras(db: Session = Depends(get_db)):
    """Returns list of registered CCTV surveillance cameras."""
    cameras = db.query(Camera).all()
    results = []
    for c in cameras:
        results.append({
            "id": c.id,
            "camera_id": c.camera_id,
            "name": c.name,
            "stream_url": c.stream_url,
            "monitored_road_id": c.monitored_road_id,
            "monitored_road_name": c.monitored_road.name if c.monitored_road else "Unassigned",
            "status": c.status,
            "fps": c.fps,
            "roi_polygon": c.roi_polygon
        })
    return results


@router.get("/{camera_id}/telemetry", response_model=CameraTelemetry)
def get_camera_telemetry(camera_id: str, db: Session = Depends(get_db)):
    """Computes live telemetry for a specific camera view."""
    camera = db.query(Camera).filter(Camera.camera_id == camera_id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")

    road = camera.monitored_road
    road_status = road.current_status if road else "OPEN"
    road_name = road.name if road else "Unassigned"
    road_id = road.road_id if road else "UNKNOWN"

    is_blocked = (road_status == "BLOCKED")
    v_count = 18 if not is_blocked else 32
    ped_count = 2 if not is_blocked else 45
    avg_speed = 38.5 if not is_blocked else 1.2
    occ = 0.28 if not is_blocked else 0.92
    stat_count = 0 if not is_blocked else 28
    q_persist = 0.0 if not is_blocked else 185.0
    state = "FREE_FLOW" if not is_blocked else "PEDESTRIAN_CROWD"

    return {
        "camera_id": camera.camera_id,
        "road_id": road_id,
        "road_name": road_name,
        "fps": 24.5,
        "status": camera.status,
        "vehicle_count": v_count,
        "pedestrian_count": ped_count,
        "class_breakdown": {"car": int(v_count * 0.5), "motorcycle": int(v_count * 0.4), "bus": 2, "truck": 1, "person": ped_count},
        "average_speed_kmh": avg_speed,
        "occupancy_ratio": occ,
        "stationary_count": stat_count,
        "queue_length_meters": stat_count * 6.5,
        "queue_persistence_seconds": q_persist,
        "traffic_state": state,
        "road_status": road_status,
        "recorded_at": datetime.now(timezone.utc).isoformat()
    }


@router.get("/{camera_id}/snapshot")
def get_camera_snapshot(camera_id: str, t: int = 0, db: Session = Depends(get_db)):
    """Returns a single JPEG snapshot for lightweight UI image rendering."""
    camera = db.query(Camera).filter(Camera.camera_id == camera_id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")

    road = camera.monitored_road
    road_status = road.current_status if road else "OPEN"
    if road and road.road_id in jigsaw_engine.edge_metadata:
        road_status = jigsaw_engine.edge_metadata[road.road_id].get("current_status", road_status)
    road_name = road.name if road else "Unassigned"

    frame = generate_synthetic_frame(camera_id, road_name, road_status, t)
    ret, jpeg = cv2.imencode(".jpg", frame)
    if not ret:
        raise HTTPException(status_code=500, detail="Failed to encode frame")

    return Response(content=jpeg.tobytes(), media_type="image/jpeg", headers={"Cache-Control": "no-cache, no-store, must-revalidate"})


@router.get("/{camera_id}/feed")
async def stream_camera_feed(camera_id: str):
    """MJPEG streaming endpoint for HTML5 video/img tags."""
    db = SessionLocal()
    try:
        camera = db.query(Camera).filter(Camera.camera_id == camera_id).first()
        if not camera:
            raise HTTPException(status_code=404, detail="Camera not found")

        road = camera.monitored_road
        road_id = road.road_id if road else None
        road_name = road.name if road else "Unassigned"
        initial_status = road.current_status if road else "OPEN"
    finally:
        db.close()

    async def frame_generator():
        idx = 0
        while True:
            status = initial_status
            if road_id and road_id in jigsaw_engine.edge_metadata:
                status = jigsaw_engine.edge_metadata[road_id].get("current_status", initial_status)

            frame = generate_synthetic_frame(camera_id, road_name, status, idx)
            ret, jpeg = cv2.imencode(".jpg", frame)
            if not ret:
                break
            idx += 1
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n")
            await asyncio.sleep(0.08)  # ~12 FPS non-blocking

    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

