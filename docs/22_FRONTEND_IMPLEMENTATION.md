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

## 2. Rendering the Real Digital Vector Road Map
The user-facing interface does **not** display abstract puzzle shapes or node-link diagrams. Instead, the UI renders a **real digital vector road map** (Google-Maps-style interactive visual presentation) using high-performance React SVG:

- **Vector Road Geometry:** Drivable road corridors are drawn as crisp, weighted vector splines matching geographic junction coordinates.
- **Dynamic Traffic State Colors:**
  - 🟢 **Green Road:** Normal flow or recommended optimal route.
  - 🟡 **Yellow Road:** Slow traffic segment.
  - 🔴 **Red Road:** Congested bottleneck corridor.
  - ⚫ **Black Road / 🚧:** Blocked segment (protest, accident, construction).
- **Map Overlays & Pins:**
  - 📍 **Start Location & Destination Pins** clearly mark origin and target junctions.
  - ➡️ **Route Highlight Path:** Animates with directional highlights along the recommended detour corridor.
- **Interactive Inspection:** Hovering or clicking on any road link displays the Selected Link HUD drawer with live camera snapshots, velocity, and occupancy metrics.


## 3. Frontend Component Architecture

`mermaid
flowchart TD
    A["App.jsx - Route Definitions"] --> B["MainLayout"]
    B --> C["Navbar - System KPIs"]
    B --> D["Sidebar - Navigation"]
    B --> E{"Active Page"}
    E --> F["Dashboard"]
    E --> G["Monitoring"]
    E --> H["RouteOptimizer"]
    E --> I["Simulator"]
    E --> J["SignalAdvisory"]

    F --> K["RealMapCanvas - Leaflet + OSM"]
    F --> L["Road Detail HUD Drawer"]
    F --> M["Disruption Ticker"]

    G --> N["MJPEG Video Grid"]
    G --> O["Detection Overlay Canvas"]

    H --> P["Route Calculator"]
    H --> Q["Detour Path Visualizer"]

    I --> R["Before/After Comparison"]
    I --> S["Redistribution Delta Table"]

    J --> T["Signal Timing Cards"]
    J --> U["Acknowledge Button"]
`

