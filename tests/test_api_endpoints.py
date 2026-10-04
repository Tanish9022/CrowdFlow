"""
End-to-End API Integration Tests for Crowd Flow.
Tests Health, Dynamic Graph, Dijkstra Routing, What-If Simulation, and Signal Recommendations.
Uses synchronous test runners with asyncio.run to guarantee execution without plugin dependencies.
Academic Prototype - SPPU CS-331-FP
"""

import sys
import os
import asyncio
import httpx

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.main import app
from app.database.session import SessionLocal
from app.graph.jigsaw_engine import jigsaw_engine


def setup_module(module):
    """Initializes and seeds graph in memory."""
    db = SessionLocal()
    try:
        jigsaw_engine.load_from_db(db)
    finally:
        db.close()


def test_health_endpoint():
    async def _run():
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "HEALTHY"
            assert data["graph_nodes"] >= 7
            assert data["graph_edges"] >= 11

    asyncio.run(_run())


def test_network_graph_endpoint():
    async def _run():
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/network/graph")
            assert response.status_code == 200
            data = response.json()
            assert len(data["nodes"]) >= 7
            assert len(data["edges"]) >= 11
            assert "total_capacity_vph" in data

    asyncio.run(_run())


def test_routing_endpoint():
    async def _run():
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            payload = {
                "source_node_id": "J_SHIVAJINAGAR",
                "target_node_id": "J_SWARGATE",
                "avoid_blocked": True,
                "calculate_alternatives": True
            }
            response = await client.post("/api/v1/routing/calculate", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert data["found"] is True
            assert data["primary_route"] is not None
            assert len(data["primary_route"]["roads"]) > 0

    asyncio.run(_run())


def test_whatif_simulation_endpoint():
    async def _run():
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            payload = {
                "blocked_road_id": "R03_JM_DECCAN",
                "disruption_type": "PROTEST"
            }
            response = await client.post("/api/v1/simulation/run", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert data["scenario_id"] == "SIM_PROTEST_R03_JM_DECCAN"
            assert data["blocked_road_id"] == "R03_JM_DECCAN"
            assert data["total_affected_roads"] > 0
            assert len(data["affected_edges"]) >= 11

    asyncio.run(_run())


def test_signal_recommendations_endpoint():
    async def _run():
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/signals/recommendations")
            assert response.status_code == 200
            recs = response.json()
            assert len(recs) >= 2
            assert "recommended_timings" in recs[0]
            assert "justification" in recs[0]

    asyncio.run(_run())


if __name__ == "__main__":
    setup_module(None)
    test_health_endpoint()
    test_network_graph_endpoint()
    test_routing_endpoint()
    test_whatif_simulation_endpoint()
    test_signal_recommendations_endpoint()
    print("[ALL TESTS PASSED SUCCESSFULLY!]")
