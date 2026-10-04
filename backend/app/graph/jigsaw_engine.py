"""
Jigsaw Road Graph Engine for Crowd Flow.
Maintains directed graph topology, calculates BPR-based dynamic impedance costs,
and handles missing jigsaw puzzle pieces when roads are blocked.
Academic Prototype - SPPU CS-331-FP
"""

import threading
import networkx as nx
from typing import Dict, List, Optional, Any, Tuple
from app.core.config import settings


class JigsawGraphEngine:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.edge_metadata: Dict[str, Dict[str, Any]] = {}
        self.node_metadata: Dict[str, Dict[str, Any]] = {}
        self.active_disruptions: List[str] = []
        self._lock = threading.Lock()

    def load_from_db(self, db_session) -> None:
        """Loads road network topology and current states from relational database."""
        from app.models.road import RoadNode, RoadEdge

        nodes = db_session.query(RoadNode).all()
        edges = db_session.query(RoadEdge).all()

        with self._lock:
            self.graph.clear()
            self.edge_metadata.clear()
            self.node_metadata.clear()
            self.active_disruptions.clear()

        id_to_node_key = {}
        for n in nodes:
            id_to_node_key[n.id] = n.node_id
            self.node_metadata[n.node_id] = {
                "id": n.id,
                "node_id": n.node_id,
                "name": n.name,
                "x": n.x,
                "y": n.y,
                "latitude": n.latitude,
                "longitude": n.longitude,
                "node_type": n.node_type
            }
            self.graph.add_node(n.node_id, **self.node_metadata[n.node_id])

        for e in edges:
            u = id_to_node_key.get(e.source_node_id)
            v = id_to_node_key.get(e.target_node_id)
            if not u or not v:
                continue

            cost = self.calculate_bpr_cost(
                distance_m=e.length_meters,
                volume_vph=e.current_vehicle_count * 10, # Extrapolate instantaneous to hourly flow
                capacity_vph=e.capacity_vph,
                avg_speed_kmh=e.current_average_speed,
                free_speed_kmh=e.free_flow_speed,
                status=e.current_status
            )

            meta = {
                "id": e.id,
                "road_id": e.road_id,
                "name": e.name,
                "source": u,
                "target": v,
                "length_meters": e.length_meters,
                "lanes": e.lanes,
                "capacity_vph": e.capacity_vph,
                "free_flow_speed": e.free_flow_speed,
                "current_status": e.current_status,
                "current_vehicle_count": e.current_vehicle_count,
                "current_average_speed": e.current_average_speed,
                "current_occupancy": e.current_occupancy,
                "dynamic_cost": cost
            }

            self.edge_metadata[e.road_id] = meta
            self.graph.add_edge(u, v, key=e.road_id, cost=cost, **meta)

            if e.current_status == "BLOCKED":
                self.active_disruptions.append(e.road_id)

    def calculate_bpr_cost(
        self,
        distance_m: float,
        volume_vph: float,
        capacity_vph: int,
        avg_speed_kmh: float,
        free_speed_kmh: float,
        status: str
    ) -> float:
        """
        Calculates Generalized Dynamic Impedance Cost:
        W(e) = distance * [1 + alpha * (q/C)^beta] * (v_free / max(v_min, v_avg)) + penalty
        """
        if status == "BLOCKED":
            return float(settings.BLOCKED_PENALTY)

        alpha = settings.BPR_ALPHA
        beta = settings.BPR_BETA
        v_min = settings.MIN_SPEED_KMH

        vc_ratio = max(0.0, volume_vph / max(1.0, float(capacity_vph)))
        speed_factor = free_speed_kmh / max(v_min, avg_speed_kmh)

        bpr_congestion_multiplier = 1.0 + alpha * (vc_ratio ** beta)
        base_cost = distance_m * bpr_congestion_multiplier * speed_factor

        # Status penalty
        penalty = 0.0
        if status == "SLOW":
            penalty = 500.0
        elif status == "CONGESTED":
            penalty = 2500.0
        elif status == "PARTIALLY_BLOCKED":
            penalty = 1500.0

        return base_cost + penalty

    def update_road_status(self, road_id: str, new_status: str, count: Optional[int] = None, speed: Optional[float] = None) -> Dict[str, Any]:
        """Dynamically updates an edge status and recalculates its graph impedance."""
        with self._lock:
            if road_id not in self.edge_metadata:
                raise ValueError(f"Road {road_id} not found in graph.")

            meta = self.edge_metadata[road_id]
            meta["current_status"] = new_status
            if count is not None:
                meta["current_vehicle_count"] = count
                meta["current_occupancy"] = min(1.0, (count * 20.0) / max(1.0, meta["length_meters"]))
            if speed is not None:
                meta["current_average_speed"] = speed

            cost = self.calculate_bpr_cost(
                distance_m=meta["length_meters"],
                volume_vph=meta["current_vehicle_count"] * 10,
                capacity_vph=meta["capacity_vph"],
                avg_speed_kmh=meta["current_average_speed"],
                free_speed_kmh=meta["free_flow_speed"],
                status=new_status
            )
            meta["dynamic_cost"] = cost

            # Update NetworkX edge attribute
            u = meta["source"]
            v = meta["target"]
            if self.graph.has_edge(u, v):
                self.graph[u][v]["cost"] = cost
                self.graph[u][v]["current_status"] = new_status
                self.graph[u][v]["dynamic_cost"] = cost

            if new_status == "BLOCKED" and road_id not in self.active_disruptions:
                self.active_disruptions.append(road_id)
            elif new_status != "BLOCKED" and road_id in self.active_disruptions:
                self.active_disruptions.remove(road_id)

            return meta

    def get_topology_dict(self) -> Dict[str, Any]:
        """Exports graph topology for frontend vector map rendering."""
        with self._lock:
            nodes = list(self.node_metadata.values())
            edges = list(self.edge_metadata.values())
            total_capacity = sum(e["capacity_vph"] for e in edges)
            avg_occ = sum(e.get("current_occupancy", 0.1) for e in edges) / max(1, len(edges))

            return {
                "nodes": nodes,
                "edges": edges,
                "active_disruptions": list(self.active_disruptions),
                "total_capacity_vph": total_capacity,
                "average_network_occupancy": round(avg_occ, 3)
            }


# Global singleton instance
jigsaw_engine = JigsawGraphEngine()
