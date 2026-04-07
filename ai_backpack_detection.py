# ==============================================================
#  AI-based Backpack Detection and Posture Simulation (Final v2)
#  Developed by: Fareedul Afrath
#  Description:
#     Detects school backpacks using YOLOv8,
#     estimates heaviness via bounding-box area ratio,
#     sends a simulated alert to a mock School App API,
#     and prepares logs for Streamlit dashboard display.
# ==============================================================

from ultralytics import YOLO
import cv2
import time
import tkinter as tk
from tkinter import messagebox
import requests
import os

# ---------------- Configuration ----------------
IMAGE_PATH = "schoolboy.png"             # input image
OUTPUT_PATH = "annotated_schoolboy.png"  # save annotated image
CONF_THRESHOLD = 0.6                     # YOLO confidence threshold
AREA_RATIO_THRESHOLD = 0.12              # heaviness threshold (tune if needed)
STUDENT_ID = "STU001"                    # mock student ID
LOG_FILE = "alerts_log.txt"              # log file used by Streamlit dashboard

# ---------------- Prepare Clean Log (optional) ----------------
# Comment this line if you want to keep old history
# open(LOG_FILE, "w").close()

# ---------------- Load YOLOv8 Model ----------------
print("[INFO] Loading YOLOv8 model...")
model = YOLO("yolov8n.pt")  # lightweight and fast model
print("[INFO] Model loaded successfully!")

# ---------------- Read Image ----------------
img = cv2.imread(IMAGE_PATH)
if img is None:
    raise FileNotFoundError(f"❌ Image not found: {IMAGE_PATH}")
print("[INFO] Image loaded successfully.")

# ---------------- Run Inference ----------------
print("[INFO] Running object detection...")
results = model(img, conf=CONF_THRESHOLD, verbose=False)
annotated_img = results[0].plot()

# ---------------- Detection and Heaviness Estimation ----------------
alert_triggered = False
heavy_alert = False
person_box = None
ratio = 0.0  # initialize for later use

# Find one person (for relative area comparison)
for box in results[0].boxes:
    cls = int(box.cls)
    label = model.names[cls].lower()
    if label == "person":
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        person_box = (x1, y1, x2, y2)
        break

# Find backpack(s) and estimate heaviness
for box in results[0].boxes:
    cls = int(box.cls)
    conf = float(box.conf)
    label = model.names[cls].lower()

    if label == "backpack" and conf >= CONF_THRESHOLD:
        alert_triggered = True
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        backpack_area = (x2 - x1) * (y2 - y1)

        # Compare to person area (if found)
        if person_box:
            px1, py1, px2, py2 = person_box
            person_area = (px2 - px1) * (py2 - py1)
            ratio = backpack_area / max(person_area, 1)
        else:
            ratio = backpack_area / (img.shape[0] * img.shape[1])

        print(f"[INFO] Backpack area ratio: {ratio:.3f}")

        if ratio > AREA_RATIO_THRESHOLD:
            heavy_alert = True
            message = f"⚠️ Heavy Backpack Detected (ratio={ratio:.2f})"
            color = (0, 0, 255)
        else:
            message = f"🎒 Normal Backpack Size (ratio={ratio:.2f})"
            color = (255, 165, 0)

        cv2.putText(
            annotated_img, message, (30, 100),
            cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 3
        )

# If no backpack detected
if not alert_triggered:
    cv2.putText(
        annotated_img, "✅ No Backpack Detected", (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3
    )

# ---------------- Mock API Alert Simulation ----------------
def send_alert_to_school_app(student_id, alert_type, ratio):
    url = "https://httpbin.org/post"  # mock API endpoint
    payload = {
        "student_id": student_id,
        "alert_type": alert_type,
        "area_ratio": round(ratio, 2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            print("[API] Alert successfully sent to School App server.")
        else:
            print(f"[API] Failed to send alert (status {response.status_code}).")
    except Exception as e:
        print("[API] Network error:", e)

# Trigger API alert if heavy
if heavy_alert:
    send_alert_to_school_app(STUDENT_ID, "HEAVY BACKPACK", ratio)

# ---------------- Log Results (Standardized Format) ----------------
with open(LOG_FILE, "a") as log:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    if heavy_alert:
        log.write(f"{timestamp} - HEAVY BACKPACK DETECTED (ratio={ratio:.2f})\n")
        print("[ALERT] Heavy Backpack Detected - Alert Sent to Teacher & Parent App")

    elif alert_triggered:
        log.write(f"{timestamp} - NORMAL BACKPACK DETECTED (ratio={ratio:.2f})\n")
        print("[INFO] Normal backpack detected.")

    else:
        log.write(f"{timestamp} - NO BACKPACK DETECTED\n")
        print("[INFO] No backpack detected.")

# ---------------- Posture Analysis Placeholder ----------------
try:
    print("[FUTURE] Posture analysis module placeholder: not executed in this version.")
    # Example (for future):
    # import mediapipe as mp
    # mp_pose = mp.solutions.pose.Pose()
    # results_pose = mp_pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # Analyze spine alignment and lean angle
except Exception as e:
    print("[POSTURE MODULE] Skipped:", e)

# ---------------- Popup Notification ----------------
try:
    root = tk.Tk()
    root.withdraw()
    if heavy_alert:
        messagebox.showinfo("Parent/Teacher Alert", "⚠️ Heavy Backpack Detected!\nAlert sent to school app.")
    elif alert_triggered:
        messagebox.showinfo("Detection Result", "🎒 Normal Backpack Size Detected.")
    else:
        messagebox.showinfo("Detection Result", "✅ No Backpack Risk Detected.")
    root.destroy()
except Exception as e:
    print("[WARNING] Popup alert failed:", e)

# ---------------- Save and Display Annotated Image ----------------
cv2.imwrite(OUTPUT_PATH, annotated_img)
print(f"[INFO] Annotated image saved as: {OUTPUT_PATH}")

cv2.imshow("AI Backpack Detection & Simulation", annotated_img)
print("[INFO] Press 'Q' to close the image window.")
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
