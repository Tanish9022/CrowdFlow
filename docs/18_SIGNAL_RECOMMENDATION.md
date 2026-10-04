# 18. Signal Recommendation

## 1. Advisory Signal Rebalancing Logic
When a road is blocked and traffic is diverted onto an alternative corridor, intersections along that detour path experience an abnormal surge in volume on one specific approach arm. Static fixed-time signal plans cause extreme queue backups on that arm.

Crowd Flow calculates an **Advisory Signal Timing Plan** to dynamically reallocate green phase time toward the overloaded detour approach.

> [!CAUTION]
> **Safety & Real-World Mandate:** The academic system produces **Advisories for Human Operator Approval**. It does not directly actuate roadside signal hardware.

## 2. Green Split Reallocation (Webster-Equisaturation Formulation)
Consider a 4-leg junction with Cycle Time $C_{\text{cycle}}$ (e.g., 90 seconds) and Lost Time $L = 8\text{ seconds}$ (yellow + all-red clearance intervals).
Total effective green time available:
$$G_{\text{total}} = C_{\text{cycle}} - L$$

Let $q_1, q_2, \dots, q_k$ be the observed or simulated critical lane volumes for the competing signal phases (e.g., Phase 1 = North-South Arterial, Phase 2 = East-West Cross Street), with saturation flows $S_1, S_2, \dots, S_k$.

The flow ratio for phase $i$ is:
$$y_i = \frac{q_i}{S_i}, \quad Y = \sum_{i=1}^k y_i$$

The recommended green phase time $g_i$ is distributed in proportion to flow ratios:
$$g_i = \left(\frac{y_i}{Y}\right) \times G_{\text{total}}$$

Subject to boundary constraints:
$$g_{\text{min}} \le g_i \le g_{\text{max}}$$
(e.g., $g_{\text{min}} = 15\text{ s}$ for pedestrian clearance, $g_{\text{max}} = 70\text{ s}$ to prevent cross-street starvation).

## 3. Example Advisory Output
```
Junction: J04 (Swargate Chowk)
Current Signal Cycle: 90s
  - Approach North-South (Detour Path): Green = 35s | Red = 55s
  - Approach East-West:                 Green = 45s | Red = 45s

Observed Disruption: Road R02 Blocked; Diverted flow +650 vph onto North-South approach.
Calculated Demand Ratio: North-South = 0.65 | East-West = 0.35

RECOMMENDED ADVISORY PLAN:
  - Approach North-South: Green = 55s (+20s) | Red = 35s
  - Approach East-West:   Green = 27s (-18s) | Red = 63s

Expected Impact: Prevents detour queue spillback by 42%; estimated average vehicle delay reduction = 18.5 seconds/veh.
```
