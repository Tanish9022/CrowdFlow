# 25. CCTV Monitoring Specification

## 1. Multi-Stream CCTV Interface
The CCTV Monitoring view displays up to 6 camera feeds concurrently in an adaptive responsive grid ($1 \times 1$, $2 \times 2$, or $3 \times 2$).

## 2. Real-Time Overlay Specification
Each camera viewport features hardware-accelerated HTML5 Canvas overlays:
- **Bounding Boxes:**
  - Cars: Neon Yellow (`#facc15`), $2\text{px}$ solid border.
  - Two-Wheelers: Electric Orange (`#fb923c`).
  - Heavy Vehicles (Buses/Trucks): Cyan (`#22d3ee`).
  - Pedestrians: Royal Purple (`#c084fc`).
- **Object Labels:** Text pill displaying `[ID: #142 | Car | 28 km/h]`.
- **ROI Boundary:** Translucent polygon with green border indicating the calibrated drivable road area.
- **Curbside Parking Boundary:** Dashed gray polygon marking the designated parking shoulder.
- **HUD Diagnostics Panel (Top-Right):**
  - Camera ID: `CAM_04_SWARGATE`
  - Stream Status: `LIVE (24.2 FPS)`
  - Active Vehicles inside ROI: `38`
  - Current Traffic State: `SIGNAL_QUEUE (Light RED: 14s remaining)`


## CCTV Monitoring Data Flow

`mermaid
flowchart LR
    CAM["CCTV Camera"] --> STREAM["MJPEG Stream Endpoint"]
    STREAM --> GRID["Multi-Camera Grid Layout"]
    GRID --> OVERLAY["Detection Overlay Canvas"]
    OVERLAY --> HUD["HUD: FPS, Count, State"]

    CAM --> YOLO["YOLOv8 Inference"]
    YOLO --> BBOX["Bounding Boxes"]
    BBOX --> TRACK["Centroid Tracker IDs"]
    TRACK --> OVERLAY
`

