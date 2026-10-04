# 32. ML Evaluation

## 1. Evaluation Methodology
In accordance with SPPU academic rigor, evaluation metrics are measured objectively against annotated ground-truth test datasets rather than fabricated numbers.

## 2. Object Detection Metrics (YOLOv8 Nano)
- **Mean Average Precision (mAP):**
  $$\text{mAP} = \frac{1}{|C|} \sum_{c \in C} \int_0^1 P_c(R) \, dR$$
- **Confusion Matrix:** Evaluated across the 5 target classes (`car`, `motorcycle`, `bus`, `truck`, `person`) and background false positives.
- **Inference Latency:** Measured in milliseconds per frame on standard CPU hardware (Intel i3/i5).

## 3. Traffic State Classification Evaluation
- **Macro F1-Score:** Harmonic mean of precision and recall across all 8 traffic states:
  $$F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$
- **State Transition Matrix:** Measures temporal stability (preventing flickering between `SLOW` and `CONGESTED` within single-frame noise).


## ML Evaluation Pipeline

`mermaid
flowchart TD
    A["Trained YOLOv8n Model"] --> B["Run inference on test set"]
    B --> C["Calculate mAP@0.5"]
    B --> D["Calculate mAP@0.5:0.95"]
    B --> E["Per-class Precision + Recall"]
    C --> F{"mAP@0.5 >= 0.75?"}
    F -- Yes --> G["Model Accepted"]
    F -- No --> H["Retrain with adjusted params"]

    I["Trained RF Classifier"] --> J["5-Fold Stratified CV"]
    J --> K["Macro F1-Score"]
    J --> L["Per-state Confusion Matrix"]
    K --> M{"F1 >= 0.88?"}
    M -- Yes --> N["Classifier Accepted"]
    M -- No --> O["Tune hyperparameters"]
`

