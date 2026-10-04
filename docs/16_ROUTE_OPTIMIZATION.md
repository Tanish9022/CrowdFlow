# 16. Route Optimization

## 1. Routing Engine Architecture
The Route Optimization engine computes optimal paths between any source junction $s \in V$ and destination junction $t \in V$ using dynamic link costs supplied by the Jigsaw Engine.

## 2. Modified Dijkstra Algorithm with Dynamic Impedance

```python
import heapq

def dijkstra_dynamic(graph, start_node, target_node):
    # Priority queue stores tuples of (current_cost, current_node, path_taken)
    pq = [(0.0, start_node, [start_node])]
    visited_costs = {node: float('inf') for node in graph.nodes}
    visited_costs[start_node] = 0.0

    while pq:
        current_cost, u, path = heapq.heappop(pq)

        if u == target_node:
            return {
                "found": True,
                "cost": current_cost,
                "path": path,
                "distance_meters": calculate_path_distance(graph, path)
            }

        if current_cost > visited_costs[u]:
            continue

        for v in graph.neighbors(u):
            edge = graph.get_edge_data(u, v)
            # If road is physically blocked, edge cost is effectively infinite
            if edge.get("status") == "BLOCKED" or edge.get("cost") >= float('inf'):
                continue

            edge_weight = edge.get("dynamic_cost", edge.get("distance_m", 100))
            new_cost = current_cost + edge_weight

            if new_cost < visited_costs[v]:
                visited_costs[v] = new_cost
                heapq.heappush(pq, (new_cost, v, path + [v]))

    return {"found": False, "cost": float('inf'), "path": [], "message": "No feasible detour route found."}
```

## 3. Alternative Multi-Path Detour Generation (K-Shortest Paths)
To prevent creating a secondary bottleneck by dumping 100% of diverted traffic onto a single alternative street, the system computes **$K$ Loopless Alternative Paths** ($K=3$) using Yen's algorithm:
- **Path 1 (Primary Detour):** Minimum impedance alternative route.
- **Path 2 (Secondary Detour):** Next best corridor utilizing an adjacent parallel arterial.
- **Path 3 (Tertiary Detour):** Outer ring bypass route for heavy multi-axle vehicles/buses.

The operator dashboard displays all $K$ alternatives with relative travel time estimations and capacity headrooms.
