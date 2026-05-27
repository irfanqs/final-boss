#!/bin/bash
# Aktifkan virtual environment
source ~/ta-env/bin/activate

# Jalankan sistem (mode normal)
python3 04_integration/pollination_system.py --version yolov11

# Mode headless (tanpa display, cocok untuk SSH)
python3 04_integration/pollination_system.py --version yolov11 --headless

# Mode dry-run (simulasi tanpa mengaktifkan GPIO)
python3 04_integration/pollination_system.py --version yolov11 --dry-run
