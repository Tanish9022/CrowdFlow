# 11. Model Training Plan

## 1. Objectives & Hardware Budget
- **Target Platform:** Intel Core i3 (Quad-Core), 8 GB RAM, CPU-only execution (or optional Google Colab T4 GPU instance for fast fine-tuning).
- **Primary Model:** YOLOv8 Nano (`yolov8n.pt`) with transfer learning from MS COCO weights.
- **Secondary Model:** Feature-based tabular classifier (Random Forest / XGBoost) for traffic state verification where rule thresholds require validation.

## 2. Object Detector Fine-Tuning Specification

### Hyperparameter Configurations
| Parameter | Value | Justification |
| :--- | :--- | :--- |
| **Base Model** | `yolov8n.pt` | Smallest footprint (3.2M params), fastest inference on CPU. |
| **Image Resolution (`imgsz`)** | 640 | Balances small two-wheeler resolution with CPU throughput. |
| **Batch Size** | 16 (GPU) / 4 (CPU) | Fits comfortably in 8 GB RAM without thrashing swap space. |
| **Epochs** | 50 | Early stopping at patience=10 prevents overfitting on small datasets. |
| **Optimizer** | AdamW | Fast convergence with weight decay ($1 \times 10^{-4}$). |
| **Initial Learning Rate ($\eta_0$)** | $0.001$ | Standard transfer learning rate with cosine annealing decay. |
| **Augmentation** | Mosaic ($0.5$), Fliplr ($0.5$), HSV ($h=0.015, s=0.7, v=0.4$) | Enhances resilience to changing sunlight, shadows, and occlusions. |

### Evaluation Metrics
- $\text{mAP}@0.5$ (Mean Average Precision at IoU 0.5)
- $\text{mAP}@0.5:0.95$ (Stricter COCO evaluation)
- Precision, Recall, and per-class F1-score for: `car`, `motorcycle`, `bus`, `truck`, `person`.

## 3. Traffic State Classifier Training (Random Forest)

### Feature Vector Input
$$\vec{x} = [N_{\text{veh}}, \bar{v}_{\text{kmh}}, \Delta v, \rho_{\text{occ}}, r_{\text{stat}}, L_{\text{queue}}, t_{\text{persist}}, N_{\text{ped}}, S_{\text{signal}}]$$
Where:
- $N_{\text{veh}}$: Total detected vehicles within road ROI
- $\bar{v}_{\text{kmh}}$: Average velocity in km/h
- $\Delta v$: Velocity variance
- $\rho_{\text{occ}}$: Bounding-box area over drivable road ROI area
- $r_{\text{stat}}$: Ratio of stationary vehicles ($\le 3 \text{ km/h}$) to total vehicles
- $L_{\text{queue}}$: Estimated queue length in meters
- $t_{\text{persist}}$: Continuous time queue has persisted (seconds)
- $N_{\text{ped}}$: Pedestrians detected on road surface
- $S_{\text{signal}}$: Signal state ($0 = \text{Green}, 1 = \text{Red}, -1 = \text{Unknown/Uncontrolled}$)

### Classifier Parameters
- Model: `RandomForestClassifier(n_estimators=100, max_depth=6, class_weight='balanced')`
- Validation Strategy: Stratified 5-Fold Cross Validation grouped by Video ID.
- Baseline Accuracy Target: $\ge 88\%$ cross-validation macro F1-score across 7 traffic states.
