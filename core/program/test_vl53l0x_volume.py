from collections import deque
import time, config
import board, busio, adafruit_vl53l0x

def distance_to_volume(d_mm: float) -> dict:
    pollen_height = max(0, config.TOF_DISTANCE_EMPTY_MM - d_mm)
    pollen_height = min(pollen_height,
                        config.TOF_DISTANCE_EMPTY_MM
                        - config.TOF_DISTANCE_FULL_MM)
    volume_mm3 = pollen_height * config.TUBE_AREA_MM2
    volume_ml  = volume_mm3 / 1000.0
    max_h      = (config.TOF_DISTANCE_EMPTY_MM
                  - config.TOF_DISTANCE_FULL_MM)
    percent    = (pollen_height / max_h * 100) if max_h > 0 else 0
    return {
        "volume_mm3": volume_mm3,
        "volume_ml":  volume_ml,
        "percent":    percent,
        "is_enough":  volume_mm3 >= config.VOLUME_MIN_THRESHOLD_MM3,
    }

i2c    = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l0x.VL53L0X(i2c)
sensor.measurement_timing_budget = 50000
window = deque(maxlen=5)

while True:
    window.append(sensor.range)
    m      = distance_to_volume(sum(window) / len(window))
    status = "CUKUP" if m["is_enough"] else "KURANG"
    print(f"vol={m['volume_ml']:.2f} mL  {m['percent']:.1f}%  [{status}]")
    time.sleep(0.3)
