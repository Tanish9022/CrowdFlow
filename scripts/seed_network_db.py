"""
Database Seeding Script for Crowd Flow.
Creates tables and seeds default Pune urban model network, cameras, signals, and users.
Production System - Crowd Flow System
"""

import os
import sys

# Ensure backend directory is in python path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.database.session import engine, SessionLocal
from app.database.base import Base
from app.models.user import User
from app.models.road import RoadNode, RoadEdge
from app.models.camera import Camera
from app.models.signal import TrafficSignal
from app.models.alert import Alert
from app.models.observation import TrafficObservation
from app.core.security import get_password_hash


def seed_database():
    print("=== Crowd Flow: Initializing and Seeding Database ===")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Seed Users
        if not db.query(User).filter_by(username="admin").first():
            admin_user = User(
                username="admin",
                full_name="Traffic Systems Administrator",
                hashed_password=get_password_hash("admin123"),
                role="ROLE_ADMIN"
            )
            operator_user = User(
                username="operator",
                full_name="TOC Operator",
                hashed_password=get_password_hash("operator123"),
                role="ROLE_OPERATOR"
            )
            db.add_all([admin_user, operator_user])
            db.commit()
            print("[OK] Default users seeded: 'admin' and 'operator'")
        
        # 2. Seed Pune Urban Road Nodes (Junctions)
        if db.query(RoadNode).count() == 0:
            nodes_data = [
                {"node_id": "J_SHIVAJINAGAR", "name": "Shivajinagar Junction", "x": 120, "y": 80, "latitude": 18.5308, "longitude": 73.8475, "node_type": "INTERSECTION"},
                {"node_id": "J_JM_NORTH", "name": "JM Road North Chowk", "x": 380, "y": 80, "latitude": 18.5285, "longitude": 73.8410, "node_type": "INTERSECTION"},
                {"node_id": "J_FC_NORTH", "name": "FC Road North (Goodluck)", "x": 640, "y": 80, "latitude": 18.5275, "longitude": 73.8380, "node_type": "INTERSECTION"},
                {"node_id": "J_KARVE_ROAD", "name": "Karve Road Gateway", "x": 120, "y": 280, "latitude": 18.5195, "longitude": 73.8330, "node_type": "INTERSECTION"},
                {"node_id": "J_DECCAN", "name": "Deccan Gymkhana Chowk", "x": 380, "y": 280, "latitude": 18.5165, "longitude": 73.8405, "node_type": "ROUNDABOUT"},
                {"node_id": "J_SWARGATE", "name": "Swargate Terminal Chowk", "x": 640, "y": 280, "latitude": 18.5018, "longitude": 73.8630, "node_type": "INTERSECTION"},
                {"node_id": "J_SB_ROAD", "name": "Senapati Bapat Bypass", "x": 380, "y": 460, "latitude": 18.5100, "longitude": 73.8300, "node_type": "HIGHWAY_MERGE"},
            ]
            node_map = {}
            for nd in nodes_data:
                node = RoadNode(**nd)
                db.add(node)
                db.flush()
                node_map[nd["node_id"]] = node

            print(f"[OK] Seeded {len(nodes_data)} road network junctions.")

            # 3. Seed Road Edges
            edges_data = [
                # Arterial Spine
                {"road_id": "R01_SHIVAJI_JM", "name": "Shivajinagar to JM North", "source": "J_SHIVAJINAGAR", "target": "J_JM_NORTH", "length": 650.0, "lanes": 3, "capacity": 1600, "speed": 50.0},
                {"road_id": "R02_JM_FC", "name": "JM North to FC North Link", "source": "J_JM_NORTH", "target": "J_FC_NORTH", "length": 550.0, "lanes": 2, "capacity": 1200, "speed": 40.0},
                {"road_id": "R03_JM_DECCAN", "name": "JM Road Arterial (Southbound)", "source": "J_JM_NORTH", "target": "J_DECCAN", "length": 1100.0, "lanes": 3, "capacity": 2200, "speed": 50.0},
                {"road_id": "R04_FC_DECCAN", "name": "FC Road Corridor", "source": "J_FC_NORTH", "target": "J_DECCAN", "length": 1200.0, "lanes": 2, "capacity": 1500, "speed": 40.0},
                
                # Feeder & Western Corridors
                {"road_id": "R05_SHIVAJI_KARVE", "name": "Shivaji to Karve Connector", "source": "J_SHIVAJINAGAR", "target": "J_KARVE_ROAD", "length": 900.0, "lanes": 2, "capacity": 1300, "speed": 45.0},
                {"road_id": "R06_KARVE_DECCAN", "name": "Karve Road to Deccan", "source": "J_KARVE_ROAD", "target": "J_DECCAN", "length": 850.0, "lanes": 2, "capacity": 1400, "speed": 40.0},
                
                # Southbound Artery to Swargate
                {"road_id": "R07_DECCAN_SWARGATE", "name": "Tilak Road to Swargate", "source": "J_DECCAN", "target": "J_SWARGATE", "length": 1400.0, "lanes": 3, "capacity": 2400, "speed": 45.0},
                {"road_id": "R08_FC_SWARGATE", "name": "FC South to Swargate Bypass", "source": "J_FC_NORTH", "target": "J_SWARGATE", "length": 2100.0, "lanes": 2, "capacity": 1400, "speed": 40.0},
                
                # Outer Bypass Loop
                {"road_id": "R09_DECCAN_SB", "name": "Deccan to Senapati Bapat", "source": "J_DECCAN", "target": "J_SB_ROAD", "length": 950.0, "lanes": 2, "capacity": 1500, "speed": 50.0},
                {"road_id": "R10_SB_SWARGATE", "name": "Senapati Bapat to Swargate Bypass", "source": "J_SB_ROAD", "target": "J_SWARGATE", "length": 1750.0, "lanes": 3, "capacity": 2100, "speed": 55.0},
                {"road_id": "R11_KARVE_SB", "name": "Karve to Senapati Bapat Link", "source": "J_KARVE_ROAD", "target": "J_SB_ROAD", "length": 1150.0, "lanes": 2, "capacity": 1200, "speed": 45.0},
            ]

            edge_map = {}
            for ed in edges_data:
                edge = RoadEdge(
                    road_id=ed["road_id"],
                    name=ed["name"],
                    source_node_id=node_map[ed["source"]].id,
                    target_node_id=node_map[ed["target"]].id,
                    length_meters=ed["length"],
                    lanes=ed["lanes"],
                    capacity_vph=ed["capacity"],
                    free_flow_speed=ed["speed"],
                    current_status="OPEN",
                    current_vehicle_count=int(ed["capacity"] * 0.25),
                    current_average_speed=ed["speed"] * 0.9,
                    current_occupancy=0.25,
                    current_dynamic_cost=ed["length"] * 1.1
                )
                db.add(edge)
                db.flush()
                edge_map[ed["road_id"]] = edge

            print(f"[OK] Seeded {len(edges_data)} directional road segments.")

            # 4. Seed CCTV Cameras
            cameras_data = [
                {"camera_id": "CAM_01", "name": "JM Road North CCTV 1", "road": "R01_SHIVAJI_JM", "stream": "synthetic_01"},
                {"camera_id": "CAM_02", "name": "FC Road Goodluck CCTV 2", "road": "R04_FC_DECCAN", "stream": "synthetic_02"},
                {"camera_id": "CAM_03", "name": "JM Road Central Artery CCTV 3", "road": "R03_JM_DECCAN", "stream": "synthetic_03"},
                {"camera_id": "CAM_04", "name": "Deccan Gymkhana Circle CCTV 4", "road": "R07_DECCAN_SWARGATE", "stream": "synthetic_04"},
                {"camera_id": "CAM_05", "name": "Karve Road Gateway CCTV 5", "road": "R06_KARVE_DECCAN", "stream": "synthetic_05"},
                {"camera_id": "CAM_06", "name": "Senapati Bapat Bypass CCTV 6", "road": "R10_SB_SWARGATE", "stream": "synthetic_06"},
            ]
            for cd in cameras_data:
                cam = Camera(
                    camera_id=cd["camera_id"],
                    name=cd["name"],
                    stream_url=cd["stream"],
                    monitored_road_id=edge_map[cd["road"]].id,
                    status="ONLINE",
                    fps=25.0,
                    roi_polygon=[[120, 150], [520, 150], [600, 580], [60, 580]]
                )
                db.add(cam)

            print(f"[OK] Seeded {len(cameras_data)} CCTV camera feeds.")

            # 5. Seed Traffic Signals
            signals_data = [
                {
                    "signal_id": "SIG_DECCAN",
                    "junction": "J_DECCAN",
                    "name": "Deccan Gymkhana Signal",
                    "cycle": 90,
                    "plan": {"NS_green": 40, "EW_green": 40, "yellow": 5, "all_red": 5}
                },
                {
                    "signal_id": "SIG_SWARGATE",
                    "junction": "J_SWARGATE",
                    "name": "Swargate Terminal Signal",
                    "cycle": 100,
                    "plan": {"NS_green": 45, "EW_green": 45, "yellow": 5, "all_red": 5}
                }
            ]
            for sd in signals_data:
                sig = TrafficSignal(
                    signal_id=sd["signal_id"],
                    junction_node_id=node_map[sd["junction"]].id,
                    junction_name=sd["name"],
                    cycle_time_seconds=sd["cycle"],
                    current_plan=sd["plan"],
                    active_phase="PHASE_NS_GREEN",
                    time_remaining_seconds=20
                )
                db.add(sig)

            print(f"[OK] Seeded {len(signals_data)} traffic signals.")
            db.commit()
            print("=== Database Seeding Completed Successfully! ===")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Database seeding failed: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

