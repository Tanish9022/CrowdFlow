# 33. Performance Optimization

## 1. CPU-Bound Optimization Strategies (Intel i3 / 8 GB RAM)
Because the target academic hardware does not assume a dedicated discrete GPU, the pipeline is engineered for extreme efficiency:

1. **Selective Frame Inference (Frame Skipping):**
   - Video is decoded at full framerate ($25-30\text{ FPS}$).
   - Heavy YOLO inference runs every $k$-th frame (e.g., $k=3$, yielding $8-10\text{ FPS}$ model inferences).
   - Centroid Kalman tracking interpolates vehicle trajectories between inference frames, maintaining smooth tracking at negligible CPU cost.
2. **Input Tensor Scaling:**
   - Default resolution set to $640 \times 640$; configurable to $480 \times 480$ on lower-tier dual-core processors.
3. **ONNX Runtime Engine:**
   - Pretrained PyTorch `.pt` weights can be exported to ONNX format with CPU-optimized vector instructions (AVX2/AVX-512).
4. **Vectorized NumPy & SciPy Operations:**
   - All spatial calculations (polygon tests, bounding box intersections) use vectorized C-extensions rather than pure Python loops.
5. **In-Memory Graph Representation:**
   - Dijkstra and network graphs are cached in memory using dictionary adjacency matrices, executing queries in $< 2\text{ milliseconds}$.
