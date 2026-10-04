# Model Training & Evaluation Suite

## Overview
This directory contains scripts for training, fine-tuning, and evaluating:
1. **Object Detection (`yolov8n`):** `train_detector.py` and `evaluate_detector.py`.
2. **Traffic Feature Extraction:** `extract_features.py` processing video clips into feature vectors.
3. **Traffic State Classifier:** `train_traffic_state.py` and `evaluate_traffic_state.py` using Random Forest / XGBoost.

## Execution Guide

### 1. Fine-Tune YOLOv8 Nano on Detection Dataset
```bash
python training/train_detector.py --data dataset/detection/data.yaml --epochs 50 --batch 8 --imgsz 640 --device cpu
```

### 2. Extract Features from Video Clips
```bash
python training/extract_features.py --video_dir dataset/traffic_state/clips --output dataset/traffic_state/extracted_features.csv
```

### 3. Train Tabular Traffic State Classifier
```bash
python training/train_traffic_state.py --features dataset/traffic_state/labels.csv --model_out models/traffic_rf_classifier.joblib
```
