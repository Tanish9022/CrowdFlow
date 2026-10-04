"""
YOLOv8 Object Detector Training Script for Crowd Flow.
Academic Prototype - SPPU CS-331-FP
"""

import argparse
from pathlib import Path


def train(data_yaml: str, epochs: int, batch: int, imgsz: int, device: str):
    print(f"=== Crowd Flow: Training YOLOv8 Object Detector ===")
    print(f"Dataset Config: {data_yaml}")
    print(f"Epochs: {epochs} | Batch: {batch} | Img Size: {imgsz} | Device: {device}")

    try:
        from ultralytics import YOLO
        model = YOLO("yolov8n.pt")  # Load pretrained baseline
        results = model.train(
            data=data_yaml,
            epochs=epochs,
            batch=batch,
            imgsz=imgsz,
            device=device,
            project="models/yolo_runs",
            name="crowd_flow_detector",
            exist_ok=True,
            verbose=True
        )
        print("Training completed successfully. Weights saved to models/yolo_runs/crowd_flow_detector/weights/best.pt")
    except ImportError:
        print("[WARNING] 'ultralytics' library is not installed in the current environment.")
        print("Run 'pip install ultralytics' to enable YOLO model training.")
    except Exception as e:
        print(f"[ERROR] Training failed: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train YOLOv8 Object Detector for Crowd Flow")
    parser.add_argument("--data", type=str, default="dataset/detection/data.yaml", help="Path to data.yaml")
    parser.add_argument("--epochs", type=int, default=50, help="Number of training epochs")
    parser.add_argument("--batch", type=int, default=8, help="Batch size")
    parser.add_argument("--imgsz", type=int, default=640, help="Image resolution")
    parser.add_argument("--device", type=str, default="cpu", help="Device (cpu or cuda:0)")
    args = parser.parse_args()

    train(args.data, args.epochs, args.batch, args.imgsz, args.device)
