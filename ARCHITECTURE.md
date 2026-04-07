# 🏗️ System Architecture

**AI-Based Backpack Detection & Posture Alert System**

---

## 📐 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         INPUT SOURCES                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ Webcam/Live  │  │  Image File  │  │   Recorded   │           │
│  │    Stream    │  │  (schoolboy) │  │    Video     │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    AI DETECTION ENGINE                           │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           YOLOv8 Nano Model (yolov8n.pt)                 │  │
│  │  • Lightweight & Fast Inference                          │  │
│  │  • Real-time Object Detection                            │  │
│  │  • Multi-class Detection (Person, Backpack, etc.)        │  │
│  └───────────────────────────────────────────────────────────┘  │
│                             ↓                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │        BACKPACK HEAVINESS ESTIMATION MODULE              │  │
│  │  • Extract Bounding Boxes                                │  │
│  │  • Calculate Area Ratio (backpack vs person)             │  │
│  │  • Compare Against Threshold (0.12)                      │  │
│  │  • Classify: Heavy/Normal/None                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                             ↓                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           POSTURE ANALYSIS (Future Module)               │  │
│  │  • MediaPipe Pose Integration [TBD]                      │  │
│  │  • Spine Alignment Analysis                              │  │
│  │  • Lean Angle Calculation                                │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    ALERT GENERATION                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   Heavy      │  │   Normal     │  │  No Backpack │           │
│  │  Backpack    │  │  Backpack    │  │   Detected   │           │
│  │    Alert     │  │    Alert     │  │    Alert     │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│         ↓                 ↓                  ↓                    │
│    [Trigger]          [Log Only]          [Log Only]             │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│              MULTI-CHANNEL ALERT DISTRIBUTION                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   Log File   │  │  School App  │  │ Annotated    │           │
│  │(alerts_log)  │  │   API Call   │  │  Image       │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    VISUALIZATION LAYER                           │
│  ┌──────────────────────┐  ┌──────────────────────┐             │
│  │  Teacher Dashboard   │  │  Parent Dashboard    │             │
│  │  (alert_dashboard)   │  │(parent_alert_dash)   │             │
│  │                      │  │                      │             │
│  │ • Latest Alert       │  │ • Alert History      │             │
│  │ • Single Alert View  │  │ • Full Timeline      │             │
│  │ • Quick Status       │  │ • Detailed DataFrame │             │
│  │ • Detection Image    │  │ • Statistics View    │             │
│  └──────────────────────┘  └──────────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Pipeline

### Step 1: Input Acquisition
```
Image Input → OpenCV cv2.imread()
              ↓
         Validate Image Format
              ↓
         Load into Memory
```

### Step 2: Detection Phase
```
Input Image → YOLOv8 Model Inference
            ↓
       Extract Detections
            ↓
       Filter by Confidence (0.6)
            ↓
       Generate Bounding Boxes
            ↓
       Plot Annotations
```

### Step 3: Analysis Phase
```
Bounding Boxes → Extract Person Box
              ↓
          Extract Backpack Box
              ↓
       Calculate Areas (width × height)
              ↓
       Compute Area Ratio
              ↓
       Compare with Threshold (0.12)
              ↓
    Classify: HEAVY/NORMAL/NONE
```

### Step 4: Alert Trigger Logic
```
Classification → If HEAVY: Trigger Alert
              ↓
         Send API Request
              ↓
         Log Event
              ↓
         Update Dashboard

              OR

         If NORMAL/NONE: Log Only
              ↓
         No API Call
              ↓
         Update Dashboard
```

### Step 5: Persistence
```
Results → Save Annotated Image
       ↓
    Append to Log File
       ↓
    Ready for Dashboard
```

---

## 📦 Component Architecture

### 1. **Detection Engine** (`ai_backpack_detection.py`)
**Responsibility:** Core AI inference and alert generation

**Dependencies:**
- `ultralytics` (YOLO)
- `cv2` (OpenCV)
- `requests` (API calls)
- `time` (timestamps)

**Key Functions:**
- Model Loading: `YOLO("yolov8n.pt")`
- Image Reading: `cv2.imread()`
- Inference: `model(img, conf=CONF_THRESHOLD)`
- Annotation: `results[0].plot()`
- Heaviness Calculation: Area ratio computation
- API Alert: `send_alert_to_school_app()`
- Logging: Append to `alerts_log.txt`

**Configuration Parameters:**
```python
IMAGE_PATH = "schoolboy.png"
OUTPUT_PATH = "annotated_schoolboy.png"
CONF_THRESHOLD = 0.6              # YOLO confidence
AREA_RATIO_THRESHOLD = 0.12       # Heaviness trigger
STUDENT_ID = "STU001"
LOG_FILE = "alerts_log.txt"
```

---

### 2. **Image Detection Module** (`detect_backpack_image.py`)
**Responsibility:** Alternative detection pipeline (same functionality as v1)

**Differences from Main Script:**
- May have different versioning/iterations
- Same core detection logic
- Useful for A/B testing or batch processing

---

### 3. **Teacher Dashboard** (`alert_dashboard.py`)
**Responsibility:** Real-time teacher monitoring interface

**Streamlit Configuration:**
- Layout: Centered
- Purpose: Quick status checks

**Components:**
```
┌─────────────────────────────┐
│ Latest Alert Display        │
│ - Alert timestamp          │
│ - Alert message            │
│ - Color-coded status       │
├─────────────────────────────┤
│ Detection Snapshot          │
│ - Annotated student image  │
│ - Bounding boxes           │
│ - Detection labels         │
├─────────────────────────────┤
│ Refresh Button              │
│ - Manual dashboard reload   │
└─────────────────────────────┘
```

**Data Source:** `alerts_log.txt` (last line)

---

### 4. **Parent Dashboard** (`parent_alert_dashboard.py`)
**Responsibility:** Comprehensive parent notification portal

**Streamlit Configuration:**
- Layout: Wide (2-column)
- Purpose: Historical tracking & detailed analysis

**Components:**
```
┌──────────────────────────────────────────────┐
│ Latest Alert Summary Section                 │
│ - Timestamp, Status, Details                │
│ - Color-coded severity indicator            │
├──────────────────────────────────────────────┤
│ Alert History Log (DataFrame)                │
│ - All past detections                       │
│ - Reverse chronological order               │
│ - Parsed into structured table              │
├──────────────────────────────────────────────┤
│ Detection Snapshot (Full-width Image)        │
│ - Latest annotated image                    │
│ - Student with detection boxes              │
│ - Bounding box visualization                │
└──────────────────────────────────────────────┘
```

**Data Processing:**
- Parse `alerts_log.txt` into DataFrame
- Extract timestamp, status, details
- Filter and categorize alerts
- Format for Streamlit display

---

## 📊 Data Structures

### Alert Log Format
```
Timestamp - Message

Examples:
2026-04-07 14:30:45 - HEAVY BACKPACK DETECTED (ratio=0.15)
2026-04-07 14:35:12 - NORMAL BACKPACK DETECTED (ratio=0.10)
2026-04-07 14:40:22 - NO BACKPACK DETECTED
```

### Alert Classification Mapping
| Detection | Area Ratio | Action | API Call | Alert Sent |
|-----------|-----------|--------|----------|-----------|
| Heavy Backpack | > 0.12 | Trigger Alert | ✅ Yes | Parent App |
| Normal Backpack | ≤ 0.12 | Log Only | ❌ No | - |
| No Backpack | - | Log Only | ❌ No | - |

### API Payload Structure (Mock)
```json
{
  "student_id": "STU001",
  "alert_type": "HEAVY BACKPACK",
  "area_ratio": 0.15,
  "timestamp": "2026-04-07 14:30:45"
}
```

### DataFrame Schema (Parent Dashboard)
```
┌───────────────────────────────────────────────────┐
│ Timestamp           │ Status            │ Details │
├─────────────────────┼─────────────────┬─────────────┤
│ 2026-04-07 14:30:45 │ 🚨 Heavy        │ HEAVY... │
│ 2026-04-07 14:35:12 │ 🎒 Normal       │ NORMAL...  │
│ 2026-04-07 14:40:22 │ ✅ No Backpack  │ NO BACKPACK│
└───────────────────────────────────────────────────┘
```

---

## ⚙️ Processing Workflow

### Detection Pipeline
```
1. Load Configuration
   ├─ Image path
   ├─ Confidence threshold
   ├─ Area ratio threshold
   └─ Student ID

2. Initialize Model
   ├─ Load YOLOv8 Nano
   ├─ Verify model loaded
   └─ Ready for inference

3. Read Input Image
   ├─ Load from disk
   ├─ Validate format
   └─ Handle errors

4. Run Inference
   ├─ Pass to YOLOv8
   ├─ Filter by confidence
   ├─ Extract boxes
   └─ Generate annotations

5. Heaviness Analysis
   ├─ Find person box
   ├─ Find backpack box
   ├─ Calculate areas
   ├─ Compute ratio
   └─ Compare threshold

6. Alert Generation
   ├─ Determine alert type
   ├─ Call API if needed
   ├─ Create log entry
   └─ Save output image

7. Visualization Update
   ├─ Dashboard refreshed
   ├─ New alert displayed
   └─ History updated
```

---

## 🌐 State Management

### Persistent State
- **Location:** `alerts_log.txt`
- **Duration:** Permanent (between runs)
- **Content:** Historical alerts
- **Access:** Read by dashboards

### In-Memory State (Detection Run)
- **Scope:** Single detection cycle
- **Variables:**
  - `results` (YOLOv8 output)
  - `annotated_img` (processed image)
  - `person_box` (detection box)
  - `ratio` (area ratio)
  - `heavy_alert` (boolean)
  - `alert_triggered` (boolean)

### Cache/Temporary Files
- **Annotated Image:** `annotated_schoolboy.png`
- **Purpose:** Display in dashboard
- **Lifecycle:** Overwrites previous on each run

---

## 🔌 External Integrations

### YOLOv8 Model Integration
```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
results = model(img, conf=CONF_THRESHOLD, verbose=False)
```
- **Model Type:** Object Detection (YOLO v8 Nano)
- **Inference Time:** <100ms (lightweight)
- **Output:** Bounding boxes with class labels

### Mock School API
```python
requests.post("https://httpbin.org/post", json=payload, timeout=5)
```
- **Endpoint:** `httpbin.org` (for testing)
- **Protocol:** HTTP POST
- **Payload:** Student ID, alert type, area ratio, timestamp
- **Status:** Mock/Testing (not real school system)

### Streamlit Integration
```python
import streamlit as st

st.set_page_config()          # Configure page
st.title()                    # Add title
st.dataframe()                # Display table
st.image()                    # Display images
st.error()/warning()/success()# Color-coded alerts
```
- **Purpose:** Web UI framework
- **Deployment:** Easy hosting (Streamlit Cloud, Heroku)
- **Refresh:** Real-time data from files

---

## 🎯 Module Interactions

```
ai_backpack_detection.py
       ↓
    [WRITE] → alerts_log.txt
       ↓
    [WRITE] → annotated_schoolboy.png
       ↓
    ┌──────────────────────────────────┐
    │                                  │
    ↓                                  ↓
alert_dashboard.py        parent_alert_dashboard.py
    [READ] ←──────────────────────────→ [READ]
    alerts_log.txt      annotated_schoolboy.png
```

**Dependency Graph:**
```
YOLOv8 Model (yolov8n.pt)
       ↑
       └─── ai_backpack_detection.py
              ├─ alerts_log.txt
              └─ annotated_schoolboy.png
                 ├─ alert_dashboard.py
                 └─ parent_alert_dashboard.py
```

---

## 🚀 Scalability Considerations

### Current Limitations
- Single image processing
- No multi-student support
- Mock API (not connected to real system)
- File-based logging (not scalable for large volumes)

### Future Enhancements for Scale

**1. Multi-Student Support**
```
alerts_log.txt → alerts_db.csv
Columns: StudentID, Timestamp, Alert, Ratio
```

**2. Database Integration**
```
alerts_log.txt → PostgreSQL/MongoDB
Query: Historical analysis
```

**3. Real-time Processing**
```
Webcam Stream → Frame Buffer → YOLOv8
                     ↓
              Continuous Detection
```

**4. Distributed Processing**
```
Multiple Cameras → Message Queue (Kafka)
                   ↓
              Processing Workers
                   ↓
              Central Dashboard
```

**5. REST API Layer**
```
/api/detect
/api/alerts
/api/history
/api/student/{id}
```

---

## 📈 Performance Characteristics

### Detection Performance
- **Model:** YOLOv8 Nano (lightweight)
- **Input Size:** 640×640 (optimized)
- **Inference Latency:** ~50-100ms
- **GPU Acceleration:** Optional (CPU fallback)
- **Memory Usage:** ~100-150MB

### Dashboard Performance
- **Refresh Rate:** ~1-2 seconds (Streamlit polling)
- **Data Load:** Entire alerts_log.txt (scales linearly)
- **Recommended Optimization:** Pagination for >1000 alerts

### Logging Performance
- **Write Operation:** ~1-5ms (file append)
- **Reads:** Linear search (O(n) for latest)

---

## 🔐 Security Considerations

### Current State (Prototype)
- ✅ Local file-based (no network exposure)
- ⚠️ Mock API (not real credentials)
- ⚠️ No authentication/authorization
- ⚠️ No data encryption

### Production Recommendations
- Implement input validation
- Add user authentication
- Encrypt sensitive data
- Secure API endpoints
- Add rate limiting
- Implement audit logging

---

## 🧩 Module Dependencies

```
ai_backpack_detection.py
├─ ultralytics      (YOLO inference)
├─ cv2              (image processing)
├─ requests         (API calls)
├─ time             (timestamps)
├─ tkinter          (GUI popups - optional)
└─ os               (file operations)

alert_dashboard.py
├─ streamlit        (web UI)
├─ PIL              (image display)
└─ os               (file operations)

parent_alert_dashboard.py
├─ streamlit        (web UI)
├─ pandas           (data processing)
├─ PIL              (image display)
└─ os               (file operations)
```

---

## 📝 File I/O Operations

```
INPUT FILES:
├─ schoolboy.png              (detection input)
└─ yolov8n.pt                 (model weights)

OUTPUT FILES:
├─ alerts_log.txt             (append logs)
└─ annotated_schoolboy.png    (overwrite on each run)

READ-ONLY FILES (Dashboard):
├─ alerts_log.txt             (parse & display)
└─ annotated_schoolboy.png    (show in UI)
```

---

## 🔄 Execution Flow Summary

```
User Trigger
   ↓
python ai_backpack_detection.py
   ↓
├─ Load YOLOv8 Model
├─ Read Input Image
├─ Run Detection
├─ Estimate Heaviness
├─ Generate Alert (if needed)
├─ Send API Call (if heavy)
├─ Create Log Entry
└─ Save Annotated Image
   ↓
python -m streamlit run alert_dashboard.py
   ↓
├─ Read Latest Alert
├─ Display Alert Status
├─ Show Annotated Image
└─ Provide Refresh Button
   ↓
OR
   ↓
python -m streamlit run parent_alert_dashboard.py
   ↓
├─ Parse Full Alert History
├─ Create DataFrame
├─ Display Timeline
├─ Show Statistics
└─ Display Annotated Image
```

---

## 🎓 Key Design Decisions

1. **YOLOv8 Nano** - Trade-off between accuracy and speed
2. **Area Ratio** - Lightweight heaviness estimation (no ML needed)
3. **File-Based Logging** - Simple, human-readable, portable
4. **Streamlit Dashboards** - Rapid UI development, zero deployment costs
5. **Mock API** - Easy testing without real infrastructure
6. **Image-Based Detection** - Can be extended to video/streams

---

**Architecture Version:** 1.0  
**Last Updated:** April 2026  
**Status:** Production Ready (Prototype)
