# 02. Problem Statement and Objectives

## 1. Problem Statement
Urban traffic management in developing metropolitan areas (such as Pune and Mumbai under SPPU jurisdiction) faces recurring crises due to sudden disruptions: public rallies, religious processions, unplanned construction, waterlogging during monsoons, and fatal traffic collisions.

Existing traffic surveillance systems in municipal command centers suffer from three major shortcomings:
1. **Visual Overload:** Hundreds of CCTV screens are monitored manually by human operators, leading to delayed detection of queue build-ups and road blockages.
2. **Detection vs. Intelligence Disconnect:** Conventional computer vision demos display bounding boxes around cars but fail to translate pixel detections into actionable traffic metrics (such as road occupancy percentage, queue persistence, and spatial-temporal stagnation).
3. **Lack of Predictive Redistribution:** When an arterial road is shut down, police deploy barricades reactively without predictive insights into how adjacent secondary roads will absorb the diverted vehicle volume, leading to cascade congestion across neighboring junctions.

## 2. Project Objectives

### Primary Objectives
1. **Automated Vision Pipeline:** Develop an edge-feasible computer vision pipeline using lightweight YOLO object detection combined with multi-object tracking (ByteTrack/centroid tracking) to calculate vehicle counts, average velocity, spatial occupancy, and stationary duration from CCTV camera feeds.
2. **Traffic-State Classification Engine:** Formulate deterministic, rule-based and machine-learning feature classification that accurately distinguishes between:
   - Free Flow
   - Normal Traffic
   - Slow Moving Traffic
   - Signal-Induced Queues (transient red light stops)
   - Heavy Congestion / Persistent Bottlenecks
   - Roadside Parked Vehicles
   - Pedestrian Crowds / Processions
3. **Dynamic Jigsaw Graph Architecture:** Construct a directed mathematical graph $G = (V, E)$ where nodes represent road junctions and edges represent road corridors with dynamic impedance cost functions derived from real-time CCTV metrics.
4. **Adaptive Route Optimization:** Implement modified Dijkstra / A* pathfinding that penalizes heavily congested segments and treats physically blocked or severed edges as having infinite impedance ($\infty$), immediately generating alternative detour paths.
5. **What-If Traffic Redistribution Simulation:** Build a transparent, explainable macroscopic traffic redistribution simulator that models how vehicle volume from a disabled road disperses across parallel links according to capacity elasticity.
6. **Advisory Signal Rebalancing:** Provide actionable recommendations for traffic signal cycle times (green split adjustments) at downstream intersections to accommodate diverted traffic surges.
7. **Unified Operator Dashboard:** Present an intuitive, high-performance web dashboard displaying real-time video overlays, network graph topology, jigsaw disruption alerts, and before-and-after simulation analytics.

## 3. Measurable Success Criteria
- Vehicle detection and tracking running at $\ge 12-15$ FPS on a modern quad-core CPU (Intel i3/i5) without requiring dedicated discrete GPUs.
- Accurate differentiation between signal queues (dispersing when light turns green) and persistent congestion queues with $>90\%$ simulated rule fidelity.
- Sub-50ms recalculation of alternative routes for a 20-node, 40-edge urban test network upon road closure.
- Zero reliance on external paid mapping APIs (Google Maps API, Mapbox) for core routing and graph operations.\n