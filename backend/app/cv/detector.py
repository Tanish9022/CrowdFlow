"""
YOLOv8 Object Detector for Crowd Flow.
Runs inference on video frames, filters mobility classes, and handles CPU frame skipping.
Academic Prototype - SPPU CS-331-FP
"""

import os
import cv2
import numpy as np
from typing import List, Dict, Any, Optional
from app.core.config import settings


class YOLOv8Detector:
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or settings.YOLO_MODEL_PATH
        self.model = None
        self.target_classes = {
            0: "person",
            1: "bicycle",
            2: "car",
            3: "motorcycle",
            5: "bus",
            7: "truck"
        }
        self.confidence_threshold = settings.CONFIDENCE_THRESHOLD
        self._load_model()

    def _load_model(self):
        try:
            from ultralytics import YOLO
            # Ultralytics will download yolov8n.pt if not locally present
            self.model = YOLO(self.model_path)
            print(f"[OK] YOLOv8 model loaded: {self.model_path}")
        except Exception as e:
            print(f"[WARNING] Could not load YOLO weights ({e}). Running in fallback mode.")
            self.model = None

    def detect(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Runs object detection on a BGR numpy frame.
        Returns list of dicts: {"bbox": [x1, y1, x2, y2], "class_name": str, "confidence": float}
        """
        if self.model is None or frame is None:
            return []

        # Run inference on resized tensor for speed
        results = self.model(frame, imgsz=640, conf=self.confidence_threshold, verbose=False)
        detections = []

        if len(results) > 0 and results[0].boxes is not None:
            boxes = results[0].boxes
            for box in boxes:
                cls_id = int(box.cls[0].item())
                if cls_id not in self.target_classes:
                    continue

                conf = float(box.conf[0].item())
                xyxy = box.xyxy[0].cpu().numpy().tolist()

                detections.append({
                    "bbox": [round(coord, 1) for coord in xyxy],
                    "class_name": self.target_classes[cls_id],
                    "confidence": round(conf, 3)
                })

        return detections


# Global detector singleton
yolo_detector = YOLOv8Detector()
