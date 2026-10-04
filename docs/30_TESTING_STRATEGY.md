# 30. Testing Strategy

## 1. Multi-Tier Testing Pyramid

```
       /\
      /  \     End-to-End System Tests (Playwright / Cypress)
     /----\    Integration Tests (Video Ingestion -> State -> Routing)
    /------\   Unit Tests (Pytest: Graph, Math, Dijkstra, Signal Splits)
```

## 2. Testing Frameworks & Tooling
- **Unit & Integration Testing:** `pytest`, `pytest-asyncio`, `pytest-cov`.
- **API Contract Testing:** `httpx` with FastAPI `TestClient`.
- **Mocking:** Synthetic video generation with OpenCV (drawing moving circles and rectangles to simulate vehicle flow and queues deterministically without needing real camera hardware during CI).

## 3. Test Coverage Goals
- **Graph & Routing Algorithms:** $100\%$ branch coverage (Dijkstra, infinite impedance, multi-path detour).
- **Traffic State Classification Rules:** $\ge 95\%$ coverage across all 8 traffic states.
- **API Endpoints:** $\ge 90\%$ coverage for authentication, routing, and simulation routers.
