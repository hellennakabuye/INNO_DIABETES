# name: Exercise
import streamlit as st
import numpy as np
import base64
from PIL import Image
import joblib


st.set_page_config(page_title="Recommended Exercises", layout="centered")
st.title("🏃‍♀️Expert Recommended Exercises")

st.sidebar.title("📖 About Diabetes")

st.sidebar.markdown(
    "Diabetes is a chronic disease that occurs when the body cannot properly process glucose."
)
st.sidebar.image("sukaali.png")

st.sidebar.markdown("### 🌐 Useful Links")
st.sidebar.markdown(
    '<a href="https://idf.org/our-network/regions-and-members/africa/members/uganda/" target="_blank">Diabetes in Uganda</a><br>'
    '<a href="https://idf.org/about-diabetes/diabetes-management/physical-activity/" target="_blank">Diabetes & Exercise</a>',
    unsafe_allow_html=True
)

st.sidebar.markdown("### 📧 Contact")
st.sidebar.markdown('<a href="mailto:hellennakabuye23@gmail.com">hellennakabuye23@gmail.com</a>', unsafe_allow_html=True)

st.markdown('**Guidelines:** Aim for 150 minutes per week, Daily movements, reduce sitting, Atleast 2 days of strength training per week<br>'
            '<br>'
            '**Aerobics:** Most useful after a meal, Walking, Cycling, Dancing, Light jogging, Skipping rope<br>'
            '<br>'
            '**Strength Training:** Increases muscle improving glucose use, Squats, Push-ups, Heavy-item lifting, Dumbbells<br>'
            '<br>'
            '**Flexibility:** Improve consistency, Yoga, Pilates, Stretches<br>'
            '<br>'
            '**Safety Tips:** <br>'
            '* Start slowly if you haven’t exercised in months.<br>'
            '* Wear comfortable shoes (especially for walking).<br>'
            '* Drink water before and after.<br>'
            '* If dizzy, stop immediately.<br>'
            '* Avoid long periods of sitting (stand every 30–60 minutes).', unsafe_allow_html=True)

# Convert local image to base64
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_base64 = get_base64_image("exer.jpg")  # ← put your image file here

st.markdown(
    f"""
    <style>
    .bottom-right-image {{
        position: fixed;
        bottom: 0px;
        right: 20px;
        height: 350px;   /* length */
        width: 350px;    /* width */
        object-fit: cover;
        z-index: 999;
    }}
    </style>

    <img src="data:image/png;base64,{img_base64}" class="bottom-right-image">
    """,
    unsafe_allow_html=True
)
