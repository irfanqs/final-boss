import cv2, time
from ultralytics import YOLO
from pathlib import Path
import config

def load_model(version: str, use_ncnn: bool = False):
    if use_ncnn:
        path = config.MODEL_PATHS_NCNN.get(version)
        if path and Path(path).exists():
            return YOLO(path, task="detect")
    path = config.MODEL_PATHS.get(version)
    if not Path(path).exists():
        raise FileNotFoundError(f"Model tidak ditemukan: {path}")
    return YOLO(path)

def run_detection(version, source, use_ncnn, save_video, show):
    model = load_model(version, use_ncnn)
    cap   = cv2.VideoCapture(source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  config.CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS,          config.CAMERA_FPS)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        t0      = time.time()
        results = model(frame, imgsz=config.IMG_SIZE,
                        conf=config.CONF_THRESHOLD,
                        iou=config.IOU_THRESHOLD,
                        device=config.DEVICE, verbose=False)
        fps       = 1.0 / (time.time() - t0)
        annotated = results[0].plot()
        cv2.putText(annotated, f"{version.upper()} | {fps:.1f} FPS",
                    (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        if show:
            cv2.imshow(f"YOLO {version}", annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()
