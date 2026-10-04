# 38. Viva Questions and Answers

## 1. Foundational Concept Questions

### Q1: Why not just use Google Maps or MapmyIndia?
**Answer:** Consumer navigation apps are designed for individual drivers, not traffic control room authorities. They optimize routes selfishly for one user without considering systemic capacity constraints. If an arterial road closes, Google Maps routes thousands of cars onto narrow residential streets, causing immediate gridlock. Crowd Flow is an operator decision-support system that models network-wide capacity, simulates traffic redistribution across multiple alternative paths, and provides signal timing advisories to prevent detour gridlock.

### Q2: How does Crowd Flow visualize traffic and what is the internal graph mechanism?
**Answer:** Crowd Flow presents a **real digital road map interface** (similar in concept to Google Maps) to operators and drivers, overlaying live traffic density (🟢 Green = Normal/Recommended, 🟡 Yellow = Slow, 🔴 Red = Congested, ⚫ Black = Blocked). Internally, the backend models the road network as a directed graph where road links have dynamic BPR impedance weights. When an incident occurs (an accident, protest, or waterlogging), the backend invalidates that edge ($W_e = \infty$), recalculates optimal detour paths using Dijkstra's algorithm, and immediately draws the newly recommended green route on the real digital map alongside advisory signal recommendations.

### Q3: Why can't YOLO directly identify traffic?
**Answer:** YOLO is an object detector, not a traffic detector. A single video frame containing 30 stationary cars could be a normal red-light queue, parked cars on a roadside, or a complete traffic breakdown. Bounding boxes alone cannot distinguish between these conditions. We require multi-object tracking over time, spatial filtering (road ROI polygons), and kinematic feature extraction (average speed, stationary fraction, queue persistence) to classify the true traffic state.

## 2. Computer Vision & ML Questions

### Q4: Why use YOLOv8 Nano (`yolov8n`)? Why not train a model from scratch?
**Answer:** Training a deep convolutional object detector from scratch requires tens of thousands of annotated images, high-end GPU clusters, and weeks of training time. YOLOv8 Nano is pretrained on the extensive MS COCO dataset, providing robust feature representations for common vehicles (cars, motorcycles, buses, trucks, pedestrians) in only 3.2 million parameters. It achieves 25–30 FPS inference on standard laptops without requiring a discrete GPU, making it ideal for our academic prototype.

### Q5: How do you distinguish between a red-light signal queue and real traffic congestion?
**Answer:** We evaluate three factors:
1. **Signal State Correlation:** If the signal is RED, stationary vehicles are classified as a `SIGNAL_QUEUE`.
2. **Dissipation on Green:** When the signal turns GREEN, a signal queue dissipates from front to back within a normal clearance cycle.
3. **Queue Persistence Time ($t_{\text{persist}}$):** If the queue persists across multiple green phases or for longer than 120 seconds with low average velocity, it transitions to `TRAFFIC_QUEUE` or `HEAVY_CONGESTION`.

### Q6: How do you prevent data leakage when training on video data?
**Answer:** In video footage, adjacent frames are virtually identical. If we randomly shuffle and split frames into train and test sets, the model simply memorizes nearly identical images, producing artificially inflated, false accuracy scores. To avoid this, we enforce **Video-Level Splitting**: entire video clips are assigned strictly to either the training set, validation set, or testing set. No frame from a training video ever appears in the test set.

## 3. Graph Theory & Algorithm Questions

### Q7: Why use Dijkstra's algorithm for routing?
**Answer:** Dijkstra's algorithm guarantees the mathematically optimal shortest path in a directed graph with non-negative edge weights. Because our urban sector graphs contain dozens of nodes and edges, Dijkstra executes in under 2 milliseconds on CPU. We enhance standard Dijkstra by replacing static distance weights with dynamic impedance costs incorporating real-time speed, road occupancy, and infinite penalties for blocked segments.

### Q8: Does your system directly control real traffic lights?
**Answer:** No. Directly actuating municipal traffic controllers involves strict legal, safety, and physical fail-safe regulations. In our academic prototype, signal timing outputs are explicitly designated as **Advisory Recommendations** for human traffic police operators to review and implement.


## Viva Topic Coverage Map

`mermaid
mindmap
    root["Crowd Flow Viva Topics"]
        Computer Vision
            YOLOv8 architecture
            Object detection vs tracking
            ROI polygon filtering
        Traffic Engineering
            Traffic state classification
            Queue persistence detection
            Webster signal timing
        Graph Theory
            Dijkstra algorithm
            Dynamic edge re-weighting
            Jigsaw missing piece analogy
        Software Engineering
            FastAPI async architecture
            React component design
            SQLite WAL concurrency
        Machine Learning
            Transfer learning rationale
            Random Forest features
            Anti-data-leakage splitting
`

