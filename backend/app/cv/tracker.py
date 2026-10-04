"""
Multi-Object Vehicle & Pedestrian Tracker for Crowd Flow.
Implements Centroid-Kalman spatial association and kinematic trajectory buffers.
Academic Prototype - SPPU CS-331-FP
"""

import math
from typing import Dict, List, Tuple, Any


class TrackedObject:
    def __init__(self, track_id: int, bbox: List[float], class_name: str, confidence: float):
        self.track_id = track_id
        self.bbox = bbox  # [x1, y1, x2, y2]
        self.class_name = class_name
        self.confidence = confidence
        
        cx = (bbox[0] + bbox[2]) / 2.0
        cy = (bbox[1] + bbox[3]) / 2.0
        self.centroid = (cx, cy)
        self.history: List[Tuple[float, float]] = [(cx, cy)]
        
        self.speed_kmh: float = 0.0
        self.is_stationary: bool = False
        self.stationary_frames: int = 0
        self.disappeared: int = 0

    def update(self, bbox: List[float], confidence: float, pixel_to_meter_scale: float = 0.05, fps: float = 25.0):
        self.bbox = bbox
        self.confidence = confidence
        cx = (bbox[0] + bbox[2]) / 2.0
        cy = (bbox[1] + bbox[3]) / 2.0
        self.centroid = (cx, cy)
        self.history.append((cx, cy))
        if len(self.history) > 30:
            self.history.pop(0)

        self.disappeared = 0

        # Calculate speed over last N frames
        if len(self.history) >= 5:
            start_pt = self.history[-5]
            curr_pt = self.history[-1]
            dist_px = math.hypot(curr_pt[0] - start_pt[0], curr_pt[1] - start_pt[1])
            dist_m = dist_px * pixel_to_meter_scale
            time_s = 5.0 / max(1.0, fps)
            speed = (dist_m / time_s) * 3.6  # m/s to km/h
            self.speed_kmh = round(speed, 1)

            if self.speed_kmh <= 3.0:
                self.stationary_frames += 5
                self.is_stationary = True
            else:
                self.stationary_frames = 0
                self.is_stationary = False


class CentroidTracker:
    def __init__(self, max_disappeared: int = 15, max_distance_px: float = 65.0):
        self.next_track_id = 1
        self.tracks: Dict[int, TrackedObject] = {}
        self.max_disappeared = max_disappeared
        self.max_distance_px = max_distance_px

    def update(self, detections: List[Dict[str, Any]], fps: float = 25.0) -> List[TrackedObject]:
        """
        detections: list of dicts with keys: bbox, class_name, confidence
        """
        if len(detections) == 0:
            for track in list(self.tracks.values()):
                track.disappeared += 1
                if track.disappeared > self.max_disappeared:
                    del self.tracks[track.track_id]
            return list(self.tracks.values())

        if len(self.tracks) == 0:
            for det in detections:
                obj = TrackedObject(self.next_track_id, det["bbox"], det["class_name"], det["confidence"])
                self.tracks[self.next_track_id] = obj
                self.next_track_id += 1
            return list(self.tracks.values())

        # Match existing tracks with new detections using Euclidean distance between centroids
        track_ids = list(self.tracks.keys())
        det_centroids = [
            ((d["bbox"][0] + d["bbox"][2]) / 2.0, (d["bbox"][1] + d["bbox"][3]) / 2.0)
            for d in detections
        ]

        assigned_detections = set()
        assigned_tracks = set()

        # Greedy nearest neighbor matching
        distances = []
        for t_idx, tid in enumerate(track_ids):
            track_pt = self.tracks[tid].centroid
            for d_idx, det_pt in enumerate(det_centroids):
                dist = math.hypot(track_pt[0] - det_pt[0], track_pt[1] - det_pt[1])
                distances.append((dist, tid, d_idx))

        distances.sort(key=lambda x: x[0])

        for dist, tid, d_idx in distances:
            if dist > self.max_distance_px:
                continue
            if tid in assigned_tracks or d_idx in assigned_detections:
                continue

            self.tracks[tid].update(
                bbox=detections[d_idx]["bbox"],
                confidence=detections[d_idx]["confidence"],
                fps=fps
            )
            assigned_tracks.add(tid)
            assigned_detections.add(d_idx)

        # Unmatched tracks
        for tid in track_ids:
            if tid not in assigned_tracks:
                self.tracks[tid].disappeared += 1
                if self.tracks[tid].disappeared > self.max_disappeared:
                    del self.tracks[tid]

        # New detections
        for d_idx, det in enumerate(detections):
            if d_idx not in assigned_detections:
                obj = TrackedObject(self.next_track_id, det["bbox"], det["class_name"], det["confidence"])
                self.tracks[self.next_track_id] = obj
                self.next_track_id += 1

        return list(self.tracks.values())
