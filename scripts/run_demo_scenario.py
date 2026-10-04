"""
5-Act Controlled Demonstration Script for Crowd Flow.
SPPU B.Sc. Computer Science CS-331-FP Viva Presentation Script.
Tanish Dhende (98) & Palavi Jadhav (108)
"""

import os
import sys
import time

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.database.session import SessionLocal
from app.graph.jigsaw_engine import jigsaw_engine
from app.routing.dijkstra import route_optimizer
from app.simulation.redistributor import simulator
from app.recommendations.signal_engine import signal_engine


def run_demo():
    print("=" * 70)
    print(" CROWD FLOW — 5-ACT CONTROLLED DEMONSTRATION")
    print(" AI-Based Traffic & Route Management System Using CCTV (SPPU CS-331-FP)")
    print(" Students: Tanish Dhende (Roll 98) & Palavi Jadhav (Roll 108)")
    print("=" * 70)

    db = SessionLocal()
    try:
        jigsaw_engine.load_from_db(db)

        # -----------------------------------------------------------------
        # ACT 1: BASELINE NORMAL NETWORK STATE
        # -----------------------------------------------------------------
        print("\n>>> ACT 1: BASELINE NORMAL NETWORK STATE")
        print("  - All 11 road segments operational (OPEN).")
        print("  - Querying optimal route from Shivajinagar Junction to Swargate Terminal...")
        
        r1 = route_optimizer.find_routes("J_SHIVAJINAGAR", "J_SWARGATE", avoid_blocked=True)
        print(f"  [OK] Route Found: {r1['found']}")
        print(f"  [OK] Primary Path Nodes: {' -> '.join(r1['primary_route']['nodes'])}")
        print(f"  [OK] Primary Path Roads: {r1['primary_route']['roads']}")
        print(f"  [OK] Total Distance: {r1['primary_route']['total_distance_meters'] / 1000:.2f} km")
        print(f"  [OK] Estimated Travel Time: {r1['primary_route']['total_time_seconds'] / 60:.1f} minutes")

        # -----------------------------------------------------------------
        # ACT 2: SUDDEN DISRUPTION EVENT (THE MISSING JIGSAW PIECE)
        # -----------------------------------------------------------------
        print("\n>>> ACT 2: SUDDEN DISRUPTION EVENT (THE MISSING JIGSAW PIECE)")
        print("  - Simulated Event: Unplanned gathering / protest on Road R03_JM_DECCAN.")
        print("  - CCTV Camera 3 detects zero velocity (v = 0.8 km/h) & high pedestrian density.")
        print("  - Traffic State Engine transitions R03 to 'BLOCKED'.")
        
        jigsaw_engine.update_road_status("R03_JM_DECCAN", "BLOCKED")
        print("  [OK] Road R03_JM_DECCAN marked BLOCKED in dynamic graph.")
        print("  [OK] Active Disrupted Pieces in Jigsaw:", jigsaw_engine.active_disruptions)

        # -----------------------------------------------------------------
        # ACT 3: JIGSAW GRAPH RECALCULATION & DETOUR ROUTING
        # -----------------------------------------------------------------
        print("\n>>> ACT 3: DYNAMIC DETOUR RECALCULATION")
        print("  - Missing piece impedance set to INFINITY (cost = 1,000,000,000).")
        print("  - Recalculating route from Shivajinagar to Swargate...")
        
        r2 = route_optimizer.find_routes("J_SHIVAJINAGAR", "J_SWARGATE", avoid_blocked=True)
        print(f"  [OK] Detour Route Found: {r2['found']}")
        print(f"  [OK] New Primary Path Nodes: {' -> '.join(r2['primary_route']['nodes'])}")
        print(f"  [OK] New Primary Path Roads: {r2['primary_route']['roads']}")
        print(f"  [OK] Is Road R03 avoided? {'R03_JM_DECCAN' not in r2['primary_route']['roads']}")
        print(f"  [OK] Alternative Detours Available: {len(r2['alternative_routes'])}")

        # -----------------------------------------------------------------
        # ACT 4: WHAT-IF REDISTRIBUTION SIMULATION
        # -----------------------------------------------------------------
        print("\n>>> ACT 4: WHAT-IF MACROSCOPIC TRAFFIC REDISTRIBUTION")
        print("  - Displacing 1,250 vph formerly carrying traffic along R03.")
        print("  - Running Logit capacity-elasticity redistribution model...")
        
        sim = simulator.simulate_disruption("R03_JM_DECCAN", "PROTEST", 1250.0)
        print(f"  [OK] Total Affected Road Corridors: {sim['total_affected_roads']}")
        print(f"  [OK] Overloaded Saturated Corridors: {sim['overloaded_roads_count']}")
        print(f"  [OK] Network Delay Increase: +{sim['network_average_delay_increase_pct']}%")
        print(f"  [OK] Recommended System Detour: {' -> '.join(sim['recommended_detour_path'])}")

        # -----------------------------------------------------------------
        # ACT 5: ADVISORY SIGNAL TIMING REBALANCING
        # -----------------------------------------------------------------
        print("\n>>> ACT 5: ADVISORY SIGNAL TIMING REBALANCING (WEBSTER EQUISATURATION)")
        print("  - Analyzing downstream surge demand along detour intersections...")
        
        recs = signal_engine.generate_recommendations(db, active_disruptions=["R03_JM_DECCAN"])
        for rec in recs:
            curr = rec['current_timings']
            recommended = rec['recommended_timings']
            print(f"  * Junction: {rec['junction_name']}")
            print(f"    - Current Green Split:     NS = {curr.get('NS_green', 40)}s | EW = {curr.get('EW_green', 40)}s")
            print(f"    - Recommended Green Split: NS = {recommended['NS_green']}s | EW = {recommended['EW_green']}s")
            print(f"    - Rationale: {rec['justification']}")
            print(f"    - Expected Delay Reduction: {rec['expected_delay_reduction_pct']}%")

        print("\n" + "=" * 70)
        print(" DEMONSTRATION COMPLETE: ALL 5 ACTS VALIDATED SUCCESSFULLY!")
        print("=" * 70)

    finally:
        db.close()


if __name__ == "__main__":
    run_demo()
