# 07. UI/UX Design System

## 1. Visual Language & Design Theme
Crowd Flow is designed as an **Industrial Municipal Traffic Operations Command Center (TOC)** dashboard. It avoids generic, bright corporate templates in favor of a focused, high-contrast **Obsidian Control Room** dark theme.

The visual language communicates:
- **Real-Time Responsiveness:** Pulsing status indicators, live telemetry readouts.
- **Safety Criticality:** High-contrast semantic traffic colors (Green = Open/Recommended, Yellow = Slow/Queue, Red = Congested, Crimson/Black = Blocked).
- **Spatial Intelligence:** Google-Maps-like real vector road network visualization overlaid with live traffic density and dynamic route highlights.

## 2. Color Palette & Design Tokens

```css
:root {
  /* Surface & Background Colors */
  --bg-primary: #0a0e17;       /* Deep obsidian canvas */
  --bg-secondary: #111827;     /* Elevated control panels */
  --bg-tertiary: #1f2937;      /* Hover surfaces & borders */
  --bg-card: rgba(17, 24, 39, 0.85); /* Glassmorphic card surface */

  /* Text & Typography */
  --text-primary: #f9fafb;     /* High-contrast crisp white */
  --text-secondary: #9ca3af;   /* Muted labels & subtitles */
  --text-muted: #6b7280;       /* Timestamps & minor legends */

  /* Semantic Traffic State Colors */
  --traffic-open: #10b981;      /* Emerald Green (Free Flow / Recommended Route) */
  --traffic-slow: #f59e0b;      /* Amber / Orange (Reduced Speed) */
  --traffic-queue: #eab308;     /* Signal-induced queue (Yellow) */
  --traffic-congested: #ef4444; /* Bright Red (Over capacity) */
  --traffic-blocked: #dc2626;   /* Deep Crimson / Black (Blocked Road Marker) */
  --traffic-crowd: #8b5cf6;     /* Purple (Pedestrian surge / Protest) */

  /* Accent & Action Colors */
  --accent-cyan: #06b6d4;      /* Telemetry, tracking IDs, graphs */
  --accent-blue: #3b82f6;      /* Primary action buttons */
  --accent-glow: rgba(6, 182, 212, 0.25);

  /* Borders & Dividers */
  --border-subtle: #1f2937;
  --border-active: #374151;
  --border-focus: #06b6d4;
}
```

## 3. Typography
- **Primary Interface Font:** `Inter`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `Roboto`, sans-serif.
- **Monospace Telemetry Font:** `JetBrains Mono`, `Fira Code`, `Consolas`, monospace (used for FPS, vehicle counts, coordinates, and cost scores).
- **Scale:**
  - Display Title: 24px / 1.2 / Semi-Bold (Dashboard Headers)
  - Section Title: 18px / 1.3 / Medium (Widget Headers)
  - Card Value: 28px / 1.1 / Bold (Metrics: Vehicle count, Speed, Delay)
  - Body Text: 14px / 1.5 / Regular
  - Meta/Caption: 12px / 1.4 / Regular (Status labels, timestamps)

## 4. UI Component Guidelines
1. **Cards & Widgets:** Rounded corners ($8\text{px}$), subtle glassmorphism border (`1px solid var(--border-subtle)`), deep drop shadows (`0 4px 20px rgba(0,0,0,0.4)`).
2. **Real Digital Road Map Rendering:** Road network rendered with crisp SVG vector geometry ($6\text{px}-10\text{px}$ strokes) matching geographic junction coordinates. Roads are dynamically color-coded: 🟢 Green (Open/Recommended), 🟡 Yellow (Slow), 🔴 Red (Congested), and ⚫ Black (Blocked).
3. **Map Markers & Route Highlights:**
   - 📍 **Start & Destination Pins** indicate origin and target junctions.
   - 🚧 **Incident Markers** highlight active protest/accident locations.
   - ➡️ **Recommended Detour Path** pulses with animated directional highlights.
4. **Buttons & Controls:** Clear hover transitions (200ms ease), focused accessibility outlines, disabled states clearly marked with 50% opacity and `cursor: not-allowed`.
5. **Alert Banners:** Non-intrusive sticky top/side notifications with dismiss and "Investigate on Map" deep-links.\n