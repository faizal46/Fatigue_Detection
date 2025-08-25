# Fatigue Identification in Driving System

## Overview
This project is aimed at detecting driver fatigue to improve road safety.  
Currently, the project has two independent modules:

1. **Software Module (Python + OpenCV):**
   - Detects drowsiness based on eye-blink/eye-closure.
   - Uses Haar Cascade / Eye aspect ratio methods for monitoring.

2. **Hardware Module (FSR 402 Sensor + Arduino/Raspberry Pi):**
   - Monitors thumb pressure on the steering wheel.
   - Drops in pressure are considered as signs of fatigue/drowsiness.

## Features
- Real-time eye closure detection using a webcam.
- Pressure sensor integration to monitor driver's hand activity.
- Modular design (software and hardware can be integrated in future).

## Tech Stack
- **Programming:** Python, Arduino IDE
- **Libraries:** OpenCV
- **Hardware:** FSR 402 Sensor, Arduino / Raspberry Pi

## Future Work
- Integrate software and hardware modules into a single system.
- Apply machine learning algorithms to improve detection accuracy.

## Author
Syed Mohamed Faizal
