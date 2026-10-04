"""
Route Optimization Engine for Crowd Flow.
Implements modified Dijkstra pathfinding with generalized BPR impedance costs,
blocked piece avoidance, and K-shortest alternative detour generation.
Academic Prototype - SPPU CS-331-FP
"""

import heapq
import networkx as nx
from typing import Dict, List, Optional, Any
from app.graph.jigsaw_engine import jigsaw_engine
from app.core.config import settings


class DynamicRouteOptimizer:
    def __init__(self, engine=None):
        self.engine = engine or jigsaw_engine

    def find_routes(
        self,
        source_node_id: str,
        target_node_id: str,
        avoid_blocked: bool = True,
        k_alternatives: int = 3
    ) -> Dict[str, Any]:
        """
        Computes primary optimal path and up to K loopless alternative detours.
        """
        G = self.engine.graph

        if source_node_id not in G.nodes:
            return {"found": False, "source_node": source_node_id, "target_node": target_node_id, "message": f"Source junction '{source_node_id}' not in network."}
        if target_node_id not in G.nodes:
            return {"found": False, "source_node": source_node_id, "target_node": target_node_id, "message": f"Target junction '{target_node_id}' not in network."}

        # Build active subgraph
        active_subgraph = nx.DiGraph()
        for u, v, data in G.edges(data=True):
            status = data.get("current_status", "OPEN")
            cost = data.get("cost", 100.0)

            # Blocked piece check
            if avoid_blocked and (status == "BLOCKED" or cost >= settings.BLOCKED_PENALTY):
                continue
            active_subgraph.add_edge(u, v, **data)

        if not nx.has_path(active_subgraph, source_node_id, target_node_id):
            return {
                "found": False,
                "source_node": source_node_id,
                "target_node": target_node_id,
                "primary_route": None,
                "alternative_routes": [],
                "message": "No feasible route found. Critical corridors are completely blocked."
            }

        # Primary route via Dijkstra
        primary_path = nx.dijkstra_path(active_subgraph, source_node_id, target_node_id, weight="cost")
        primary_route = self._build_route_option(primary_path, active_subgraph, route_name="Primary Route", is_primary=True)

        # Generate K-Shortest alternative paths using Yen's algorithm
        alternatives = []
        try:
            # nx.shortest_simple_paths generates paths in ascending order of weight
            path_generator = nx.shortest_simple_paths(active_subgraph, source_node_id, target_node_id, weight="cost")
            count = 0
            for alt_path in path_generator:
                if alt_path == primary_path:
                    continue
                count += 1
                alt_route = self._build_route_option(
                    alt_path,
                    active_subgraph,
                    route_name=f"Alternative Detour {count}",
                    is_primary=False,
                    is_detour=True
                )
                alternatives.append(alt_route)
                if count >= k_alternatives:
                    break
        except Exception:
            pass

        return {
            "found": True,
            "source_node": source_node_id,
            "target_node": target_node_id,
            "primary_route": primary_route,
            "alternative_routes": alternatives,
            "message": f"Optimal route calculated successfully ({len(alternatives)} detours available)."
        }

    def _build_route_option(self, path_nodes: List[str], graph: nx.DiGraph, route_name: str, is_primary: bool, is_detour: bool = False) -> Dict[str, Any]:
        segments = []
        roads = []
        total_dist = 0.0
        total_time = 0.0
        total_cost = 0.0

        for i in range(len(path_nodes) - 1):
            u = path_nodes[i]
            v = path_nodes[i + 1]
            edge_data = graph[u][v]

            road_id = edge_data.get("road_id", f"{u}_{v}")
            road_name = edge_data.get("name", road_id)
            dist = edge_data.get("length_meters", 500.0)
            speed_kmh = max(2.0, edge_data.get("current_average_speed", 40.0))
            cost = edge_data.get("cost", dist)
            status = edge_data.get("current_status", "OPEN")

            time_s = (dist / (speed_kmh * 1000 / 3600))

            segments.append({
                "from_node": u,
                "to_node": v,
                "road_id": road_id,
                "road_name": road_name,
                "status": status,
                "distance_meters": round(dist, 1),
                "estimated_time_seconds": round(time_s, 1),
                "cost": round(cost, 2)
            })

            roads.append(road_id)
            total_dist += dist
            total_time += time_s
            total_cost += cost

        return {
            "route_name": route_name,
            "nodes": path_nodes,
            "roads": roads,
            "segments": segments,
            "total_distance_meters": round(total_dist, 1),
            "total_time_seconds": round(total_time, 1),
            "total_cost": round(total_cost, 2),
            "is_primary": is_primary,
            "is_detour": is_detour
        }


route_optimizer = DynamicRouteOptimizer()
