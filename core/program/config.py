from pathlib import Path

BASE_DIR   = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR   = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

MODEL_PATHS = {
    "yolov11": str(MODELS_DIR / "yolov11_best.pt"),
}
MODEL_PATHS_NCNN = {
    "yolov11": str(MODELS_DIR / "yolov11_best_ncnn_model"),
}

# GPIO (BCM numbering)
PIN_SERVO      = 18
PIN_BLOWER     = 13
PIN_STATUS_LED = 25
VL53L0X_I2C_ADDR = 0x29

SERVO_FREQ_HZ      = 50
SERVO_ANGLE_CLOSED = 0
SERVO_ANGLE_OPEN   = 90

BLOWER_FREQ_HZ      = 1000
BLOWER_DUTY_DEFAULT = 80

# Kamera
CAMERA_SOURCE = 0
CAMERA_WIDTH  = 640
CAMERA_HEIGHT = 480
CAMERA_FPS    = 30
USE_PICAMERA2 = False

# YOLO inferensi
IMG_SIZE       = 320
CONF_THRESHOLD = 0.5
IOU_THRESHOLD  = 0.45
TARGET_CLASS   = "matang"
DEVICE         = "cpu"

# Tabung pollen (silinder diameter 40 mm, tinggi 80 mm)
TUBE_DIAMETER_MM = 40.0
TUBE_HEIGHT_MM   = 80.0
TUBE_AREA_MM2    = 3.14159 * (TUBE_DIAMETER_MM / 2) ** 2

TOF_DISTANCE_EMPTY_MM    = 80
TOF_DISTANCE_FULL_MM     = 10
VOLUME_MIN_THRESHOLD_MM3 = 5000

# Logika penyemprotan
SPRAY_DURATION_SEC       = 2.0
COOLDOWN_AFTER_SPRAY_SEC = 3.0
MIN_DETECTION_FRAMES     = 3

LOG_CSV_PATH = LOGS_DIR / "pollination_log.csv"
