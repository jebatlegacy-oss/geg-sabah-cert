import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io
import random
import string
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

st.set_page_config(page_title="GEG Cert Gen", page_icon="🏆", layout="centered")

st.markdown("""
<style>
.main { background-color: #f8fafc; }
.stButton>button {
    width: 100%; background-color: #4F46E5; color: white;
    font-weight: bold; padding: 0.75rem; border-radius: 1rem;
}
.header-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem; border-radius: 1rem; text-align: center;
    margin-bottom: 2rem; color: white;
}
.success-box {
    background-color: #d1fae5; border: 2px solid #6ee7b7;
    padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;
}
.warning-box {
    background-color: #fef3c7; border: 2px solid #fbbf24;
    padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <h1>🏆 GEG Sabah Cert Generator</h1>
    <p style="font-size: 0.9rem;">Created by Ts.Jebat | <a href="http://www.jebatlegacy.vip" target="_blank" style="color: white; text-decoration: underline;">www.jebatlegacy.vip</a></p>
    <p style="font-size: 0.8rem;">GEG Sabah x GEG Kelantan Collaboration</p>
</div>
""", unsafe_allow_html=True)

# ===== EMAIL CONFIGURATION =====
EMAIL_SENDER = "jebatlegacy@gegkotakinabalu.edu.my"
EMAIL_PASSWORD = "xeit neeg ounj jnwv"
# ================================

def generate_cert_id():
    prefix = "GEG"
    year = datetime.now().year
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{pref
