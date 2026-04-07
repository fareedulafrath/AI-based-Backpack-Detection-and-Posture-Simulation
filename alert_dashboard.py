# ==============================================================
#  Streamlit Dashboard – AI Backpack & Posture Alert System
#  Developed by: Fareedul Afrath
#  Description:
#     Displays detection results from alerts_log.txt and
#     the annotated student image for teacher/parent view.
# ==============================================================

import streamlit as st
from PIL import Image
import os

# ---------------- Basic Setup ----------------
st.set_page_config(page_title="School AI Alert System", layout="centered")
st.title("🎒 AI-Based Backpack & Posture Alert Dashboard")
st.markdown("---")

LOG_FILE = "alerts_log.txt"
IMAGE_FILE = "annotated_schoolboy.png"

# ---------------- Function to Get Latest Alert ----------------
def read_latest_alert():
    if not os.path.exists(LOG_FILE):
        return None
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    return lines[-1].strip() if lines else None

latest_alert = read_latest_alert()

# ---------------- Display Alert ----------------
if latest_alert:
    st.subheader("📢 Latest Alert Information")
    st.text(latest_alert)

    # Analyze alert type
    if "HEAVY" in latest_alert.upper():
        st.error("⚠️ Heavy Backpack Detected! Alert sent to Parent App.")
    elif "NORMAL" in latest_alert.upper():
        st.warning("🎒 Normal Backpack Detected – No risk observed.")
    elif "NO BACKPACK" in latest_alert.upper():
        st.success("✅ No Backpack Detected – Student Safe.")
    else:
        st.info("ℹ️ Waiting for detection results...")

else:
    st.info("No alerts found yet. Please run the detection script first.")

# ---------------- Display Annotated Image ----------------
if os.path.exists(IMAGE_FILE):
    st.markdown("### 🧒 AI Detection Snapshot")
    img = Image.open(IMAGE_FILE)
    st.image(img, caption="Detected student image with bounding boxes", use_column_width=True)
else:
    st.warning("⚠️ No annotated image found. Run the detection script first.")

# ---------------- Refresh Button ----------------
if st.button("🔄 Refresh Alert"):
    st.experimental_rerun()

# ---------------- Footer ----------------
st.markdown("---")
st.caption("Developed by Fareedul Afrath | AI & Data Science | Prototype Simulation")
