# 01. Project Vision

## 1. Executive Summary
**Crowd Flow** is an AI-based traffic and route management decision-support prototype that monitors urban road networks through CCTV video feeds, detects traffic bottlenecks, represents the road grid as an adaptive "jigsaw" graph, and simulates the ripple effects of road closures. When a road is compromised by protests, VIP movements, accidents, waterlogging, or severe congestion, Crowd Flow treats that road as a missing puzzle piece, recalculates alternative routes avoiding saturated links, simulates the redistribution of displaced vehicles, and recommends optimized traffic signal splits for traffic police operators.

## 2. Academic & Institutional Context
- **Institution:** Savitribai Phule Pune University (SPPU)
- **Degree:** Bachelor of Science in Computer Science (T.Y. B.Sc. CS)
- **Course Code:** CS-331-FP (Project Work)
- **Academic Year:** 2025–2026 / 2026–2027
- **Project Team:**
  - Tanish Dhende (Roll No. 98)
  - Palavi Jadhav (Roll No. 108)

## 3. Core Philosophy: The Dynamic Jigsaw Metaphor
Traditional navigation applications (such as Google Maps or MapmyIndia) treat road navigation from an egocentric point of view: finding the fastest path for a single driver without considering systemic capacity constraints. When a major arterial corridor closes, naive rerouting dumps thousands of vehicles onto narrow residential feeder roads, causing secondary gridlock.

Crowd Flow models the urban traffic network as a **dynamic jigsaw puzzle**:
1. **Nodes (Intersections):** Fixed vertices where traffic splits or converges.
2. **Edges (Road Segments):** Dynamic jigsaw pieces with finite physical vehicle capacities, current densities, and flow rates.
3. **Missing Piece (Disruption Event):** When a segment is blocked, that piece is removed from the usable graph.
4. **Jigsaw Fit (Traffic Redistribution):** Traffic cannot vanish; the volume displaced from the missing piece must be distributed across remaining corridors without exceeding critical capacity thresholds ($V/C > 0.85$).
5. **Advisory Rebalancing:** To assist the newly loaded detour corridors, the system generates signal timing advisories (e.g., extending green phase time along detour arterial corridors).

## 4. Key Distinctions
| Feature | Generic CCTV Project | Standard Navigation App | Crowd Flow Academic System |
| :--- | :--- | :--- | :--- |
| **Primary Goal** | Count vehicles in a frame | Reroute single vehicle | Network-wide traffic balance & decision support |
| **AI Role** | Object detection bounding boxes | GPS probe aggregation | Spatial-temporal tracking, queue persistence, road state classification |
| **Graph Dynamics** | Static or nonexistent | Commercial proprietary API | Explicit directed graph with real-time capacity-impedance functions |
| **Disruption Handling** | None | Reactive rerouting | Proactive "What-If" redistribution simulation |
| **Signal Control** | None | None | Capacity-aware advisory signal phase splits |

## 5. System Statement
> "Crowd Flow converts CCTV observations into a dynamic representation of a road network. It detects and tracks vehicles, extracts movement and queue features, determines the state of individual roads, and represents those roads as a dynamic graph. When a road becomes blocked or overloaded, the system treats it as a missing piece in the traffic jigsaw, recalculates feasible routes through the remaining network, simulates traffic redistribution, and generates route and signal recommendations for an operator."\n