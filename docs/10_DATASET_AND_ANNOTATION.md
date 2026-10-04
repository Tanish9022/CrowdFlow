# 10. Dataset and Annotation

## 1. Academic Dataset Strategy
Consistent with SPPU CS-331-FP guidelines and realistic student computing constraints:
1. **Pretrained Baseline:** Use standard COCO weights for initial detection validation.
2. **Targeted Fine-Tuning Dataset:** A curated, project-specific dataset of Indian urban traffic scenes (Pune roads such as Shivajinagar, JM Road, FC Road, Swargate) comprising **300–800 annotated frames** if fine-tuning is required.
3. **Traffic State Classification Dataset:** A collection of **50–100 video clips** (5 to 15 seconds each) capturing specific operational states.

## 2. Annotation Formats & Directory Layout

### 2.1 Object Detection Dataset (YOLO Format)
Each image file has a corresponding `.txt` file with normalized bounding boxes:
`<class_id> <x_center> <y_center> <width> <height>`

```
dataset/
├── detection/
│   ├── data.yaml
│   ├── images/
│   │   ├── train/  # 70% of footage
│   │   ├── val/    # 15% of footage
│   │   └── test/   # 15% of footage
│   └── labels/
│       ├── train/
│       ├── val/
│       └── test/
```

#### `data.yaml` Schema
```yaml
path: ../dataset/detection
train: images/train
val: images/val
test: images/test

names:
  0: person
  1: motorcycle
  2: car
  3: bus
  4: truck
```

### 2.2 Video-Level Splitting Rule (Anti-Leakage)
> [!CRITICAL]
> **Data Leakage Prevention:** In video-based machine learning, adjacent frames in the same video clip are almost identical. Randomly splitting individual frames into train and test sets leads to artificial, fabricated accuracy scores ($>99\%$) that collapse in real life.
> **Rule:** Whole videos must be assigned to either `train`, `val`, or `test`. No frame from Video A may ever appear in the validation or test sets if Video A was used in training.

### 2.3 Traffic State Classification Dataset
A structured CSV dataset linking extracted temporal features to ground-truth traffic states:
```csv
clip_id,camera_id,vehicle_count,avg_speed,occupancy_ratio,stationary_ratio,queue_persistence_s,pedestrian_count,ground_truth_state
clip_001.mp4,CAM_01,42,4.2,0.88,0.76,65.0,2,HEAVY_CONGESTION
clip_002.mp4,CAM_01,12,38.5,0.22,0.00,0.0,0,FREE_FLOW
clip_003.mp4,CAM_02,30,1.5,0.75,0.85,25.0,1,SIGNAL_QUEUE
clip_004.mp4,CAM_03,4,0.0,0.40,1.00,180.0,120,PEDESTRIAN_CROWD
clip_005.mp4,CAM_04,0,0.0,0.00,0.00,0.0,0,BLOCKED
```\n