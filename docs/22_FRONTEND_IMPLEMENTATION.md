# 22. Frontend Implementation

## 1. Frontend Architecture & Directory Layout
The frontend is built using React 18 with a clean component-based layout:

```
frontend/
├── src/
│   ├── main.jsx             # React entrypoint
│   ├── App.jsx              # App root & route definitions
│   ├── index.css            # Obsidian design tokens & global styles
│   ├── layouts/
│   │   ├── MainLayout.jsx   # Topbar, sidebar navigation, alert drawer
│   │   └── AuthLayout.jsx   # Minimal authentication shell
│   ├── pages/
│   │   ├── Dashboard.jsx    # Main operations dashboard
│   │   ├── Monitoring.jsx   # Multi-CCTV video grid with overlays
│   │   ├── JigsawMap.jsx    # Signature interactive vector road network
│   │   ├── Simulator.jsx    # What-If redistribution comparison view
│   │   ├── Routing.jsx      # Detour and alternative path planner
│   │   ├── Signals.jsx      # Advisory signal timing screen
│   │   ├── Analytics.jsx    # Time-series graphs & heatmaps
│   │   └── Settings.jsx     # Thresholds, ROI calibration & camera config
│   ├── components/
│   │   ├── common/          # Buttons, Modal, Badge, Tooltip, Card
│   │   ├── video/           # MJPEG / Video player canvas with detection overlays
│   │   ├── graph/           # SVG-based dynamic Jigsaw road network
│   │   └── telemetry/       # Live KPI cards, sparklines, queue indicators
│   ├── hooks/
│   │   ├── useTelemetry.js  # WebSocket subscription to live updates
│   │   └── useRoadGraph.js  # Graph topology state manager
│   ├── api/
│   │   └── client.js        # Axios instance with JWT interceptors
│   ├── types/               # Type definitions & prop-types
│   └── utils/               # Color interpolation, geometry, time formatting
```

## 2. Rendering the Signature Interactive Jigsaw Map
The Jigsaw Map is rendered using high-performance SVG (Scalable Vector Graphics) directly in React:
- **Junction Nodes:** Rendered as interactive circular SVG nodes with junction badges (`<circle>`, `<text>`).
- **Road Links:** Rendered as directed vector splines (`<path d="..." />`) with stroke widths corresponding to road capacity and stroke colors bound dynamically to real-time status (`GREEN` for Open, `CRIMSON` for Blocked).
- **Missing Puzzle Piece Effect:** When an edge is marked `BLOCKED`, the line transitions to an animated dashed pattern (`stroke-dasharray="8 6"`) with a red pulsating outline and a missing jigsaw puzzle cutout icon centered on the road link.
