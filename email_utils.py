import smtplib
from email.message import EmailMessage
import streamlit as st

def send_email_alert(to_email, result, confidence):
    sender_email = st.secrets["EMAIL"]
    app_password = st.secrets["APP_PASSWORD"]

    msg = EmailMessage()
    msg["Subject"] = "Deepfake Detection Alert"
    msg["From"] = sender_email
    msg["To"] = to_email

    msg.set_content(f"""
Hello,

Your video has been analyzed.

Result       : {result}
Confidence   : {round(confidence * 100, 2)} %

Thank you for using Deepfake Detection System.
""")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
    except:
        st.error("Email sending failed")