"""
Traffic State Classification Engine for Crowd Flow.
Implements the core AI principle: Vehicle Detection != Traffic Detection.
Combines kinematic features, spatial occupancy, queue persistence, and signal state
to classify real-world operational traffic states.
Academic Prototype - SPPU CS-331-FP
"""

from typing import Dict, List, Optional, Any
from app.cv.tracker import TrackedObject
from app.cv.roi import SpatialROIFilter


class TrafficStateEngine:
    def __init__(self):
        # Persistence tracking: {road_id: continuous_seconds_in_queue}
        self.queue_timers: Dict[str, float] = {}
        self._clf = None
        self._model_attempted = False

    def _get_classifier(self):
        if not self._model_attempted:
            self._model_attempted = True
            try:
                import os
                import joblib
                import warnings
                model_path = os.path.join(os.path.dirname(__file__), "../../../models/traffic_rf_classifier.joblib")
                if os.path.exists(model_path):
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        self._clf = joblib.load(model_path)
            except Exception:
                self._clf = None
        return self._clf

    def evaluate(
        self,
        road_id: str,
        tracks: List[TrackedObject],
        roi_filter: SpatialROIFilter,
        signal_state: str = "GREEN", # GREEN, RED, UNCONTROLLED
        frame_dt_seconds: float = 1.0
    ) -> Dict[str, Any]:
        """
        Evaluates a frame's tracked objects and returns structured traffic telemetry.
        """
        # 1. Filter objects inside drivable road ROI vs curbside parking
        road_vehicles = []
        parked_vehicles = []
        pedestrians_on_road = []

        class_breakdown = {"car": 0, "motorcycle": 0, "bus": 0, "truck": 0, "person": 0}

        for t in tracks:
            cls = t.class_name
            if cls in class_breakdown:
                class_breakdown[cls] += 1

            if cls == "person":
                if roi_filter.is_inside_road(t.centroid):
                    pedestrians_on_road.append(t)
            else:
                # Vehicle
                if roi_filter.is_in_parking_zone(t.centroid) and t.is_stationary:
                    parked_vehicles.append(t)
                elif roi_filter.is_inside_road(t.centroid):
                    road_vehicles.append(t)

        total_active_vehicles = len(road_vehicles)
        total_pedestrians = len(pedestrians_on_road)

        # 2. Kinematic Feature Extraction
        speeds = [v.speed_kmh for v in road_vehicles]
        avg_speed = sum(speeds) / max(1, total_active_vehicles) if road_vehicles else 45.0
        stationary_vehicles = [v for v in road_vehicles if v.is_stationary]
        stationary_count = len(stationary_vehicles)
        stationary_ratio = stationary_count / max(1, total_active_vehicles)

        # Road Area Occupancy Ratio (Bounding boxes area / ROI area)
        roi_area = roi_filter.compute_roi_area()
        vehicle_box_areas = sum((v.bbox[2] - v.bbox[0]) * (v.bbox[3] - v.bbox[1]) for v in road_vehicles)
        occupancy_ratio = min(1.0, vehicle_box_areas / max(1.0, roi_area))

        # Queue length approximation (meters)
        queue_length_m = stationary_count * 6.5  # Approx 6.5m per queued vehicle slot

        # Queue Persistence Duration
        current_persist = self.queue_timers.get(road_id, 0.0)
        if stationary_ratio >= 0.50 and total_active_vehicles >= 3:
            current_persist += frame_dt_seconds
        else:
            current_persist = max(0.0, current_persist - (frame_dt_seconds * 1.5))
        self.queue_timers[road_id] = current_persist

        # 3. Traffic State Classification
        traffic_state = "NORMAL"
        road_status = "OPEN"
        
        try:
            clf = self._get_classifier()
            if clf is not None:
                # feature order: vehicle_count, avg_speed_kmh, occupancy_ratio, stationary_ratio, queue_persistence_s, pedestrian_count
                features = [[
                    total_active_vehicles,
                    avg_speed,
                    occupancy_ratio,
                    stationary_ratio,
                    current_persist,
                    total_pedestrians
                ]]
                prediction = clf.predict(features)
                traffic_state = prediction[0]
                
                # Derive road_status
                if traffic_state in ["PEDESTRIAN_CROWD", "HEAVY_CONGESTION"]:
                    road_status = "BLOCKED"
                elif traffic_state == "TRAFFIC_QUEUE":
                    road_status = "CONGESTED"
                elif traffic_state in ["SIGNAL_QUEUE", "SLOW"]:
                    road_status = "SLOW"
                else:
                    road_status = "OPEN"
            else:
                raise FileNotFoundError("Model file not found or failed to load")
                
        except Exception as e:
            # Fallback to Decision Rules if model loading fails
            # Case A: Pedestrian Crowd / Protest Rally
            if total_pedestrians >= 12 and (total_pedestrians > total_active_vehicles * 1.5):
                traffic_state = "PEDESTRIAN_CROWD"
                road_status = "BLOCKED"
            # Case B: Free Flow (Low density, high speed)
            elif occupancy_ratio < 0.25 and avg_speed >= 35.0:
                traffic_state = "FREE_FLOW"
                road_status = "OPEN"
            # Case C: Parked Vehicles Non-Traffic
            elif len(parked_vehicles) >= 4 and total_active_vehicles <= 2:
                traffic_state = "PARKED"
                road_status = "OPEN"
            # Case D: Heavy Congestion / Blockage (Persistent Jam)
            elif current_persist >= 120.0 and avg_speed <= 5.0 and stationary_ratio >= 0.70:
                traffic_state = "HEAVY_CONGESTION"
                road_status = "BLOCKED"
            # Case E: Traffic Queue (Persistent queue beyond signal clearance)
            elif current_persist >= 60.0 and stationary_ratio >= 0.50:
                traffic_state = "TRAFFIC_QUEUE"
                road_status = "CONGESTED"
            # Case F: Signal-Induced Queue (Transitory stop at red light)
            elif signal_state.upper() == "RED" and stationary_ratio >= 0.60 and current_persist < 60.0:
                traffic_state = "SIGNAL_QUEUE"
                road_status = "SLOW"
            # Case G: Slow Traffic
            elif avg_speed < 20.0 or occupancy_ratio >= 0.60:
                traffic_state = "SLOW"
                road_status = "SLOW"
            else:
                traffic_state = "NORMAL"
                road_status = "OPEN"

        return {
            "road_id": road_id,
            "vehicle_count": total_active_vehicles,
            "pedestrian_count": total_pedestrians,
            "parked_count": len(parked_vehicles),
            "class_breakdown": class_breakdown,
            "average_speed_kmh": round(avg_speed, 1),
            "occupancy_ratio": round(occupancy_ratio, 2),
            "stationary_count": stationary_count,
            "stationary_ratio": round(stationary_ratio, 2),
            "queue_length_meters": round(queue_length_m, 1),
            "queue_persistence_seconds": round(current_persist, 1),
            "traffic_state": traffic_state,
            "road_status": road_status
        }


traffic_state_engine = TrafficStateEngine()
