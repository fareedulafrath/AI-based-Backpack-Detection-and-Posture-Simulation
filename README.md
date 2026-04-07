# 🎒 AI-Based Backpack Detection & Posture Alert System

**Developed by:** Fareedul Afrath | B.Tech AI & DS

---

## 📋 Project Overview

A smart AI-powered system that detects and analyzes school backpacks in student images using YOLOv8. The system estimates backpack heaviness, triggers alerts based on predefined thresholds, and provides real-time dashboards for teachers and parents to monitor student safety and posture health.

### Key Features

- ✅ **YOLOv8-based Object Detection** – Lightweight and fast backpack/person detection
- ⚖️ **Heaviness Estimation** – Uses bounding-box area ratio to estimate backpack weight
- 📢 **Automated Alert System** – Sends alerts when heavy backpacks are detected
- 📊 **Streamlit Dashboards** – Interactive dashboards for teachers and parents
- 📝 **Alert Logging** – Persistent logging of all detection events
- 🖼️ **Annotated Output** – Saves annotated images with detection boxes

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenCV
- YOLOv8 (pre-trained model)
- Streamlit
- Pandas
- PIL

### Installation

```bash
pip install ultralytics opencv-python streamlit pandas pillow requests
```

### Running the Detection Script

```bash
python ai_backpack_detection.py
```

The script will:
1. Load the YOLOv8 model
2. Detect persons and backpacks in the input image
3. Estimate backpack heaviness
4. Log results to `alerts_log.txt`
5. Save annotated image

### Running the Dashboards

**Teacher Dashboard:**
```bash
streamlit run alert_dashboard.py
```

**Parent Dashboard:**
```bash
streamlit run parent_alert_dashboard.py
```

---

## 📁 Project Structure

```
PostureSimulation/
├── ai_backpack_detection.py       # Main detection script (Final v2)
├── detect_backpack_image.py       # Alternative detection module
├── alert_dashboard.py             # Teacher alert dashboard
├── parent_alert_dashboard.py      # Parent alert dashboard (Final v3)
├── alerts_log.txt                 # Detection alerts log
├── yolov8n.pt                     # YOLOv8 nano model (pre-trained)
└── README.md                      # This file
```

---

## 🔧 Configuration

Edit the configuration section in `ai_backpack_detection.py`:

```python
IMAGE_PATH = "schoolboy.png"             # Input image path
OUTPUT_PATH = "annotated_schoolboy.png"  # Annotated output image
CONF_THRESHOLD = 0.6                     # YOLO confidence (0-1)
AREA_RATIO_THRESHOLD = 0.12              # Heaviness threshold (tune as needed)
STUDENT_ID = "STU001"                    # Mock student ID
LOG_FILE = "alerts_log.txt"              # Log file path
```

---

## 📊 Alert Classification

The system generates three types of alerts:

| Status | Criteria | Action |
|--------|----------|--------|
| 🚨 **Heavy Backpack** | Area ratio > threshold | Alert sent to parent app |
| 🎒 **Normal Backpack** | Area ratio ≤ threshold | No alert |
| ✅ **No Backpack** | Person detected, no backpack | No alert |

---

## 📈 Dashboard Features

### Teacher Dashboard (`alert_dashboard.py`)
- Latest alert display
- Alert categorization with emojis
- Annotated student image preview
- Real-time status updates

### Parent Dashboard (`parent_alert_dashboard.py`)
- Full alert history with timestamps
- Parsed DataFrame view of all alerts
- Latest alert summary
- Annotated detection images
- Wide layout for comprehensive monitoring

---

## 📝 Log Format

Alerts are logged in `alerts_log.txt` with the following format:

```
YYYY-MM-DD HH:MM:SS - [BACKPACK DETECTION] Student STU001: NORMAL BACKPACK DETECTED (Area Ratio: 0.10)
YYYY-MM-DD HH:MM:SS - [BACKPACK DETECTION] Student STU001: HEAVY BACKPACK DETECTED (Area Ratio: 0.15)
YYYY-MM-DD HH:MM:SS - [BACKPACK DETECTION] Student STU001: NO BACKPACK DETECTED
```

---

## 🎯 Use Cases

- **School Safety Monitoring** – Track student backpack weight to prevent health issues
- **Posture Analysis** – Identify students carrying excessively heavy backpacks
- **Parent Notifications** – Real-time alerts to parents about potential health risks
- **Administrative Tracking** – Historical data for school health initiatives

---

## ⚙️ Model Information

- **Model:** YOLOv8 Nano (`yolov8n.pt`)
- **Framework:** Ultralytics
- **Optimized For:** Speed and accuracy balance
- **Detection Classes:** Person, backpack, and other common objects

---

## 📌 Future Enhancements

- Real posture angle analysis using pose estimation
- Multi-frame temporal analysis for accuracy
- Email/SMS notifications integration
- Machine learning-based heaviness prediction
- Web API for school management systems
- Mobile app integration

---

## 📄 License

This project is developed for educational and school safety purposes.

---

## 📧 Contact

For questions or suggestions, please reach out to the developer.

---

**Last Updated:** April 2026
"# AI-based-Backpack-Detection-and-Posture-Simulation" 
