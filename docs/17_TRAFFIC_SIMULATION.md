# 17. Traffic Simulation

## 1. Macroscopic What-If Simulation Model
Crowd Flow implements a transparent, controlled macroscopic traffic redistribution model. It simulates the systemic redistribution of vehicle flow across the network when one or more road links are severed or throttled.

## 2. Mathematical Redistribution Formulation
Let road link $e_b \in E$ be marked `BLOCKED`.
Let $Q_{\text{displaced}} = q(e_b)$ be the vehicular volume (vehicles/hour) that previously utilized $e_b$.

### Capacity-Elasticity Weight Allocation
The diverted traffic is distributed across $M$ candidate alternative detour paths $\{P_1, P_2, \dots, P_M\}$ connecting the upstream diversion point to downstream convergence junctions.

The proportion of flow $\gamma_m$ assigned to alternative path $P_m$ is governed by a Logit discrete-choice model based on available residual capacity $C_{\text{res}}(P_m)$ and path impedance $W(P_m)$:
$$\gamma_m = \frac{\exp(-\theta \cdot W(P_m)) \cdot C_{\text{res}}(P_m)}{\sum_{j=1}^M \exp(-\theta \cdot W(P_j)) \cdot C_{\text{res}}(P_j)}$$
Where $\theta$ is the route sensitivity dispersion parameter (default: $\theta = 0.005$).

### Projected Volume & Occupancy Calculation
For each edge $e$ participating in detour path $P_m$:
$$q_{\text{simulated}}(e) = q_{\text{baseline}}(e) + \sum_{m: e \in P_m} \gamma_m \cdot Q_{\text{displaced}}$$
The simulated occupancy ratio is:
$$\rho_{\text{simulated}}(e) = \min\left(1.0, \, \rho_{\text{baseline}}(e) + \frac{\Delta q(e)}{C(e)}\right)$$

## 3. Before vs. After Simulation Telemetry Output
When an operator executes a simulation, the service produces a comparative delta:
```json
{
  "scenario_id": "SIM_PROTEST_JM_01",
  "blocked_road": "R_JM_NORTH",
  "displaced_volume_vph": 1250,
  "summary": {
    "total_affected_roads": 4,
    "overloaded_roads_count": 1,
    "average_network_delay_increase_percent": 24.8
  },
  "edges_comparison": [
    {
      "road_id": "R_FC_ROAD",
      "baseline_occupancy": 0.55,
      "simulated_occupancy": 0.88,
      "status_before": "NORMAL",
      "status_after": "CONGESTED",
      "is_overloaded": true
    },
    {
      "road_id": "R_SENAPATI_BAPAT",
      "baseline_occupancy": 0.32,
      "simulated_occupancy": 0.49,
      "status_before": "OPEN",
      "status_after": "OPEN",
      "is_overloaded": false
    }
  ]
}
```
