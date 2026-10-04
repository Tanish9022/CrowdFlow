# Dataset Directory

## Overview
This directory houses datasets used for:
1. **Object Detection:** Targeted fine-tuning of YOLOv8 for local urban Indian traffic conditions (Pune roads).
2. **Traffic State Classification:** Short video clips and extracted tabular features mapped to operational states.

## Directory Layout
```
dataset/
├── README.md
├── detection/
│   ├── data.yaml            # YOLOv8 dataset configuration
│   ├── images/
│   │   ├── train/           # Training frames (70%)
│   │   ├── val/             # Validation frames (15%)
│   │   └── test/            # Testing frames (15%)
│   └── labels/
│       ├── train/           # YOLO format bounding box txt files
│       ├── val/
│       └── test/
└── traffic_state/
    ├── README.md
    ├── clips/               # 5-15s MP4 clips representing each traffic state
    ├── labels.csv           # Master tabular dataset linking clips to states
    ├── train.csv            # 70% video-level split
    ├── val.csv              # 15% video-level split
    └── test.csv             # 15% video-level split
```

## Anti-Leakage Protocol
Strict video-level partitioning is maintained: all frames or sub-clips from a specific recording session belong exclusively to either train, val, or test.
