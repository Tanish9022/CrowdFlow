# 36. Demo Scenario

## 1. The Definitive SPPU Viva Demonstration Walkthrough
The end-to-end oral examination demo is structured as a clear 5-act narrative demonstrating every layer of the system:

### Act 1: Baseline Normal Network State
- Operator opens the dashboard (`http://localhost:5173`).
- All 6 road segments in the Pune Model Network show `GREEN (OPEN)` or `EMERALD (NORMAL)`.
- CCTV feeds display smooth simulated vehicular flow.
- A standard route query from Junction 1 to Junction 6 selects the direct corridor via Road $R_3$ (Total travel time: 3.5 minutes).

### Act 2: Sudden Disruption Event (Protest / Accident)
- On Road $R_3$ (JM Road North), a simulated protest rally or multi-vehicle collision occurs.
- CCTV feed for Camera 3 shows vehicles slowing to zero velocity, dense pedestrian clusters on the road, and queue persistence exceeding 120 seconds.
- The Traffic State Engine automatically flags Road $R_3$ as `BLOCKED`.
- Dashboard triggers a red alert ticker: **"CRITICAL DISRUPTION DETECTED: ROAD R3 (JM ROAD) COMPROMISED"**.

### Act 3: Dynamic Graph Recalculation & Real Map Rerouting
- The real digital road map instantly updates: Road $R_3$ turns black with a 🚧 roadblock marker.
- Dynamic impedance weight $W(R_3)$ is updated to $\infty$ in the backend graph engine.
- The route optimization engine recalculates the optimal path from Junction 1 to Junction 6: Road $R_3$ is avoided; the system highlights the new recommended green detour corridor via $J_1 \to J_4 \to J_5 \to J_6$ (Roads $R_4, R_6, R_7$).

### Act 4: What-If Redistribution Simulation
- The operator navigates to the Simulation tab to investigate downstream impact.
- Clicks "Simulate Disruption: 100% of R3 Flow Diverted".
- The simulation engine renders the comparative before-and-after view:
  - Road $R_6$ occupancy jumps from $35\%$ to $86\%$ (`CONGESTED`).
  - Junction 5 approach experiences extreme queue pressure.

### Act 5: Advisory Signal Rebalancing
- The system automatically generates an Advisory Signal Timing Plan for Junction 5:
  - North-South green phase increased from $35\text{ s}$ to $55\text{ s}$ (+20s).
  - Cross-street green phase adjusted to maintain cycle balance.
- Operator clicks "Acknowledge & Implement Advisory".
- Summary telemetry shows simulated detour delay reduced by $38\%$.
