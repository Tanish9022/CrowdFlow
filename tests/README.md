# Test Suite — Crowd Flow

## Test Organization
- `tests/unit/`: Unit tests for graph calculations, Dijkstra algorithm, traffic state rules, Webster signal splits, and BPR cost formulas.
- `tests/integration/`: End-to-end integration tests connecting simulated video feeds, feature extraction, graph updates, and REST API endpoints.
- `tests/edge_cases/`: Specialized tests for edge cases (empty roads, red lights, complete network partition, missing cameras).

## Running Tests
```bash
pytest tests/ -v
```
