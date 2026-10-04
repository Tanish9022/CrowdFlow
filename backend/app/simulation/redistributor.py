"""
What-If Macroscopic Traffic Redistribution Simulator for Crowd Flow.
Simulates network flow redistribution when one or more road pieces are severed/blocked.
Academic Prototype - SPPU CS-331-FP
"""

import math
from typing import Dict, List, Optional, Any
from app.graph.jigsaw_engine import jigsaw_engine
from app.routing.dijkstra import route_optimizer


class WhatIfSimulator:
    def __init__(self, engine=None):
        self.engine = engine or jigsaw_engine

    def simulate_disruption(
        self,
        blocked_road_id: str,
        disruption_type: str = "PROTEST",
        custom_volume_vph: Optional[float] = None,
        theta: float = 0.005
    ) -> Dict[str, Any]:
        """
        Executes macroscopic redistribution simulation for a disabled road link.
        """
        if blocked_road_id not in self.engine.edge_metadata:
            raise ValueError(f"Road {blocked_road_id} not found in network.")

        target_edge = self.engine.edge_metadata[blocked_road_id]
        displaced_flow = custom_volume_vph if custom_volume_vph is not None else float(target_edge["current_vehicle_count"] * 10)
        displaced_flow = max(100.0, displaced_flow)

        u = target_edge["source"]
        v = target_edge["target"]

        # 1. Capture baseline state
        baseline_edges = {}
        for rid, emeta in self.engine.edge_metadata.items():
            baseline_edges[rid] = {
                "road_id": rid,
                "name": emeta["name"],
                "capacity": emeta["capacity_vph"],
                "base_vol": float(emeta["current_vehicle_count"] * 10),
                "base_occ": emeta.get("current_occupancy", 0.25),
                "base_speed": emeta.get("current_average_speed", 45.0),
                "status_before": emeta.get("current_status", "OPEN")
            }

        # 2. Find alternative detour corridors from u to v (or whole network) avoiding blocked_road_id
        # Temporarily mark target edge as blocked
        previous_status = target_edge["current_status"]
        self.engine.update_road_status(blocked_road_id, "BLOCKED")

        routing_result = route_optimizer.find_routes(u, v, avoid_blocked=True, k_alternatives=3)
        candidate_paths = []
        if routing_result["found"] and routing_result["primary_route"]:
            candidate_paths.append(routing_result["primary_route"])
        candidate_paths.extend(routing_result.get("alternative_routes", []))

        # 3. Calculate redistribution choice probabilities via Logit model
        # γ_m = exp(-θ * W_m) * C_res(P_m) / Sum(...)
        path_weights = []
        for path in candidate_paths:
            path_cost = path["total_cost"]
            # Residual capacity = min(capacity - baseline_volume) across links in path
            min_residual = min(
                (baseline_edges[r]["capacity"] - baseline_edges[r]["base_vol"])
                for r in path["roads"] if r in baseline_edges
            )
            residual_cap = max(50.0, float(min_residual))
            weight = math.exp(-theta * (path_cost / 100.0)) * residual_cap
            path_weights.append(weight)

        total_weight = sum(path_weights) if path_weights else 1.0
        probabilities = [(w / total_weight) for w in path_weights] if path_weights else []

        # 4. Allocate diverted flow to candidate road links
        flow_deltas = {rid: 0.0 for rid in baseline_edges}
        for path, prob in zip(candidate_paths, probabilities):
            allocated_flow = prob * displaced_flow
            for r in path["roads"]:
                flow_deltas[r] += allocated_flow

        # 5. Compile simulated telemetry output
        edge_deltas = []
        overloaded_count = 0
        total_delay_increase = 0.0

        for rid, base in baseline_edges.items():
            if rid == blocked_road_id:
                edge_deltas.append({
                    "road_id": rid,
                    "road_name": base["name"],
                    "baseline_volume_vph": round(base["base_vol"], 1),
                    "simulated_volume_vph": 0.0,
                    "volume_delta_vph": -round(base["base_vol"], 1),
                    "capacity_vph": base["capacity"],
                    "baseline_occupancy": round(base["base_occ"], 2),
                    "simulated_occupancy": 1.0,
                    "status_before": base["status_before"],
                    "status_after": "BLOCKED",
                    "is_overloaded": True,
                    "baseline_speed_kmh": round(base["base_speed"], 1),
                    "simulated_speed_kmh": 0.0
                })
                continue

            delta_v = flow_deltas.get(rid, 0.0)
            sim_vol = base["base_vol"] + delta_v
            cap = max(1, base["capacity"])
            sim_occ = min(1.0, (sim_vol / cap))

            # BPR speed degradation: v_sim = v_free / (1 + 0.15 * (sim_vol / cap)^4)
            free_speed = self.engine.edge_metadata[rid]["free_flow_speed"]
            vc_ratio = sim_vol / cap
            sim_speed = max(3.0, free_speed / (1.0 + 0.15 * (vc_ratio ** 4.0)))

            status_after = "OPEN"
            if sim_occ >= 0.85:
                status_after = "CONGESTED"
                overloaded_count += 1
            elif sim_occ >= 0.65:
                status_after = "SLOW"

            is_overloaded = sim_occ >= 0.85

            edge_deltas.append({
                "road_id": rid,
                "road_name": base["name"],
                "baseline_volume_vph": round(base["base_vol"], 1),
                "simulated_volume_vph": round(sim_vol, 1),
                "volume_delta_vph": round(delta_v, 1),
                "capacity_vph": cap,
                "baseline_occupancy": round(base["base_occ"], 2),
                "simulated_occupancy": round(sim_occ, 2),
                "status_before": base["status_before"],
                "status_after": status_after,
                "is_overloaded": is_overloaded,
                "baseline_speed_kmh": round(base["base_speed"], 1),
                "simulated_speed_kmh": round(sim_speed, 1)
            })

            if delta_v > 0:
                speed_drop_pct = max(0.0, (base["base_speed"] - sim_speed) / base["base_speed"])
                total_delay_increase += speed_drop_pct * 100.0

        # Restore original status in engine so simulation is a "what-if" sandbox
        self.engine.update_road_status(blocked_road_id, previous_status)

        affected_count = len([e for e in edge_deltas if abs(e["volume_delta_vph"]) > 5.0])
        avg_delay_pct = round(total_delay_increase / max(1, affected_count), 1)

        primary_detour_roads = candidate_paths[0]["roads"] if candidate_paths else []

        return {
            "scenario_id": f"SIM_{disruption_type.upper()}_{blocked_road_id}",
            "disruption_type": disruption_type,
            "blocked_road_id": blocked_road_id,
            "blocked_road_name": target_edge["name"],
            "displaced_volume_vph": round(displaced_flow, 1),
            "total_affected_roads": affected_count,
            "overloaded_roads_count": overloaded_count,
            "network_average_delay_increase_pct": avg_delay_pct,
            "affected_edges": edge_deltas,
            "recommended_detour_path": primary_detour_roads
        }


simulator = WhatIfSimulator()
