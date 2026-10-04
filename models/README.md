# Models Directory

## Model Artifacts Management
Large binary weight files (`*.pt`, `*.onnx`, `*.joblib`, `*.engine`) are excluded from Git revision control via `.gitignore` to keep the repository lightweight.

## Expected Models
1. **`yolov8n.pt`**: Baseline Ultralytics YOLOv8 Nano weights for object detection.
   - Automatically downloaded by Ultralytics on first execution or placed manually.
2. **`crowd_flow_yolo_best.pt`**: Fine-tuned YOLOv8 weights on local traffic datasets.
3. **`traffic_rf_classifier.joblib`**: Serialized Random Forest traffic state classifier trained on extracted feature vectors.

## How to Download Baseline Model
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```
