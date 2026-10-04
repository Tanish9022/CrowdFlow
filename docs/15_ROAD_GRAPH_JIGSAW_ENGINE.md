# 15. Road Graph Jigsaw Engine

## 1. Graph Theoretical Representation
The urban road network is modeled as a weighted directed multigraph $G = (V, E)$:
- **Vertices ($V$):** Physical road intersections and major decision junctions:
  $$V = \{v_1, v_2, \dots, v_n\}$$
  Each vertex possesses geographical or grid coordinates: $v_i = (\text{id}, \text{name}, x, y, \text{type})$.
- **Directed Edges ($E$):** Drivable road segments connecting junctions:
  $$e_k = (u, v, k) \in E \quad \text{where } u, v \in V$$
  Edge attributes include:
  $$\text{attr}(e_k) = \{\text{road\_id}, \text{length\_m}, \text{lanes}, \text{capacity\_vph}, v_{\text{free}}, \rho(t), \bar{v}(t), \text{status}\}$$

## 2. The Jigsaw Puzzle Metaphor in Graph Theory
In a classic jigsaw puzzle, every interlocking piece must fit to maintain structural continuity. In urban traffic:
1. Each road segment $e_k$ is an active "puzzle piece" carrying dynamic vehicle flow $q(e_k)$.
2. When an edge is declared `BLOCKED` (e.g., due to an accident or protest on $e_{\text{blocked}}$), that piece is conceptually **removed from the puzzle**.
3. Removing $e_{\text{blocked}}$ creates an impedance void: the cost of traversing $e_{\text{blocked}}$ becomes:
   $$W(e_{\text{blocked}}) = \infty$$
4. The volume $q(e_{\text{blocked}})$ formerly carried by the disabled link cannot vanish; it must be assembled into neighboring puzzle pieces (parallel corridors) without exceeding their structural capacities.

```
       [Junction 1] ───(Road R1: Open)───► [Junction 2]
            │                                   │
      (Road R4: Open)                    (Road R2: Heavy)
            │                                   ▼
            ▼                            [Junction 4]
       [Junction 3] ───[Road R3: BLOCKED]───► (Missing Piece)
                         (Detour diverted via R4 & R5)
```

## 3. Dynamic Edge Weight (Cost) Formula
Crowd Flow does not route purely on physical distance $d(e)$. Edge cost represents **Generalized Impedance** incorporating delay, congestion, and capacity saturation:

$$W(e) = d(e) \cdot \left[ 1 + \alpha \cdot \left(\frac{q(e)}{C(e)}\right)^\beta \right] \cdot \left( \frac{v_{\text{free}}(e)}{\max(v_{\text{min}}, \bar{v}(e))} \right) + \Omega(e)$$

Where:
- $d(e)$: Physical road length in meters.
- $q(e)$: Observed or estimated vehicle volume (vehicles/hour).
- $C(e)$: Practical capacity of the road segment (vehicles/hour).
- $\alpha, \beta$: Standard BPR (Bureau of Public Roads) calibration coefficients (default: $\alpha = 0.15, \beta = 4.0$).
- $v_{\text{free}}(e)$: Design free-flow speed (e.g., $50\text{ km/h}$).
- $\bar{v}(e)$: Current real-time average speed measured via CCTV.
- $v_{\text{min}}$: Speed lower-bound threshold ($2.0\text{ km/h}$) to prevent division by zero.
- $\Omega(e)$: Penalty term:
  $$\Omega(e) = \begin{cases} 0 & \text{if status is OPEN} \\ 500 & \text{if status is SLOW} \\ 2000 & \text{if status is CONGESTED} \\ \infty & \text{if status is BLOCKED} \end{cases}$$
