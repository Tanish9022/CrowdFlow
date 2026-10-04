"""
Spatial Region-of-Interest (ROI) and Parking Zone Filters for Crowd Flow.
Uses Point-in-Polygon geometric tests to isolate drivable road corridors from curbside parking.
Academic Prototype - SPPU CS-331-FP
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional


class SpatialROIFilter:
    def __init__(self, roi_polygon: Optional[List[List[float]]] = None, parking_polygon: Optional[List[List[float]]] = None):
        self.roi_polygon = np.array(roi_polygon, dtype=np.int32) if roi_polygon else None
        self.parking_polygon = np.array(parking_polygon, dtype=np.int32) if parking_polygon else None

    def is_inside_road(self, point: Tuple[float, float]) -> bool:
        """Tests whether (x, y) centroid lies inside the drivable road ROI."""
        if self.roi_polygon is None or len(self.roi_polygon) < 3:
            return True # If no ROI defined, default to whole frame

        result = cv2.pointPolygonTest(self.roi_polygon, (float(point[0]), float(point[1])), False)
        return result >= 0

    def is_in_parking_zone(self, point: Tuple[float, float]) -> bool:
        """Tests whether (x, y) centroid is inside the designated curbside parking shoulder."""
        if self.parking_polygon is None or len(self.parking_polygon) < 3:
            return False

        result = cv2.pointPolygonTest(self.parking_polygon, (float(point[0]), float(point[1])), False)
        return result >= 0

    def compute_roi_area(self) -> float:
        """Calculates total pixel area of drivable road ROI."""
        if self.roi_polygon is None or len(self.roi_polygon) < 3:
            return 640.0 * 480.0
        return float(cv2.contourArea(self.roi_polygon))
