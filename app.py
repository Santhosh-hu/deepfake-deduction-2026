import streamlit as st
import pandas as pd
import tempfile
import re
import os


from db import *
from email_utils import send_email_alert
from model_utils import predict_video
from video_utils import extract_face_frames

st.set_page_config(page_title="Deepfake Detection", layout="wide")

ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]

# ---------- INIT DATABASE ----------
create_users_table()
create_history_table()

# ---------- LOGIN ----------
def login_page():
    st.title("Login")

    email = st.text_input("Enter your Email")

    col1, col2 = st.columns(2)

    with col1:
        user_login = st.button("User Login")

    with col2:
        admin_login = st.button("Login as Admin")

    if user_login:
        if email == "":
            st.warning("Please enter your email")
            return

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            st.error("Invalid Email Format")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (email) VALUES (?)", (email,))
            conn.commit()
        except:
            pass
        conn.close()

        st.session_state["logged_in"] = True
        st.session_state["user_email"] = email
        st.session_state["is_admin"] = False
        st.rerun()

    if admin_login:
        admin_password = st.text_input("Enter Admin Password", type="password")
        if admin_password:
            if admin_password == ADMIN_PASSWORD:
                st.session_state["logged_in"] = True
                st.session_state["is_admin"] = True
                st.rerun()
            else:
                st.error("Wrong password")

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

if not st.session_state["logged_in"]:
    login_page()
    st.stop()

# ---------- DASHBOARD ----------
st.title("Deepfake Detection Dashboard")

# ---------- SIDEBAR ----------
st.sidebar.title("Dashboard")

if st.session_state["is_admin"]:
    st.sidebar.success("Admin Logged In")
else:
    st.sidebar.success("User Logged In")

st.sidebar.write("---")

# LOGOUT
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["is_admin"] = False
    st.session_state["user_email"] = ""
    st.rerun()

# ---------- ADMIN ----------
if st.session_state["is_admin"]:
    st.subheader("User Activity History")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT email, result, confidence, created_at 
        FROM history 
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "Email": row[0],
            "Result": row[1],
            "Confidence (%)": round(row[2]*100, 2),
            "Time": row[3]
        })

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

    st.stop()

# ---------- USER UI ----------
uploaded_video = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])

if uploaded_video:
    st.success("Video uploaded")

    if st.button("Start Detection"):

        # TEMP FILE SAVE
        with tempfile.NamedTemporaryFile(delete=False) as tfile:
            tfile.write(uploaded_video.read())
            video_path = tfile.name

        st.video(video_path)

        st.subheader("Video Frames")

        # FACE FRAMES
      frames = extract_face_frames(video_path)

      if len(frames) == 0:
          st.warning(" No frames detected")
      else:
          frames = frames[:8]

          cols = st.columns(4)
          for i, frame in enumerate(frames):
              cols[i % 4].image(frame, use_container_width=True)

        st.info("Analyzing...")

        # PREDICTION
        label, confidence = predict_video(video_path)

        # CLEANUP
        if os.path.exists(video_path):
            os.remove(video_path)

        # STORE HISTORY
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO history (email, result, confidence) VALUES (?, ?, ?)",
            (st.session_state.get("user_email", "unknown"), label, confidence)
        )

        conn.commit()
        conn.close()

        # EMAIL ALERT
        if label == "FAKE" and "user_email" in st.session_state:
            send_email_alert(
                st.session_state["user_email"],
                label,
                confidence
            )

        # FINAL RESULT
        st.markdown(f"""
        ### Final Result
        - Prediction: **{label}**
        - Confidence: **{confidence*100:.2f}%**
        """)
