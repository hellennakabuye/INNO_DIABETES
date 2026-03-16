import streamlit as st
import numpy as np
import base64
import joblib
from PIL import Image

# ---------------- ACCESS CONTROL ---------------- #

# List of authorized organizations
# You update this after payment
AUTHORIZED_ORGS = {
    "6wner": "2027-02-20",
    "ZXCVF": "2026-06-30",
    "ERTTY": "2026-03-01"
}

# Get organization from URL
query_params = st.query_params
org = query_params.get("org")

if not org:
    # Load image
    col1, col2, col3 = st.columns(3)

    with col2:
        st.image("sukaali.png", width=500)

    st.error("🔒 Access Restricted")
    st.markdown(
    'This tool is licensed to partner health organizations.<br>'
    '<br>'
    'If you represent a clinic, Researcher or NGO, please contact:<br>'
    '<br>'
    '📧 sukaalicheckug@gmail.com<br>'
    '📞 +256 703145793',unsafe_allow_html=True

    )
    st.subheader("Thank You For Visiting SukaaliCheck!")
    st.stop()

if org not in AUTHORIZED_ORGS:
    st.error("🚫 Organization Not Authorized")
    st.stop()

expiry_date = datetime.strptime(AUTHORIZED_ORGS[org], "%Y-%m-%d")

if datetime.now() > expiry_date:
    st.error("⛔ Subscription Expired")
    st.markdown("Please renew your institutional subscription.")
    st.stop()

# If all checks pass:
st.success(f"✅ Licensed Access: {org.replace('_', ' ').title()}")

st.set_page_config(page_title="Recommended Diet", layout="centered")
st.title("🍏Expert Recommended Diet")

st.sidebar.title("📖 About Diabetes")

st.sidebar.markdown(
    "Diabetes is a chronic disease that occurs when the body cannot properly process glucose."
)
st.sidebar.image("sukaali.png")

st.sidebar.markdown("### 🌐 Useful Links")
st.sidebar.markdown(
    '<a href="https://idf.org/our-network/regions-and-members/africa/members/uganda/" target="_blank">Diabetes in Uganda</a><br>'
    '<a href="https://medlineplus.gov/diabeticdiet.html" target="_blank">Diabetes & Diet</a>',
    unsafe_allow_html=True
)

st.sidebar.markdown("### 📧 Contact")
st.sidebar.markdown('<a href="mailto:sukaalicheckug@gmail.com">sukaalicheckug@gmail.com</a>', unsafe_allow_html=True)


st.markdown('**Diet Guidelines:** low added sugar, high fiber, balanced carbs, lean proteins, and healthy fats.<br>'
            '<br>'  
            ' **General Principles:** Focus on slow-digesting carbs, include protein in every meal, avoid processed foods, and aim for portion control<br>'
            '<br>'
            ' **Breakfasts:** Katogo(Matooke, Beans, Ddodo/Nakati), Combo(Tea, 2 Bread slices, 1 Boiled egg), Fruity(1 Banana, 1 Boiled egg, 2 spoons of Gnuts)<br>'
            '<br>'
            ' **Lunch:** Classic(Posho, Beans, Nakati), Sweet(SweetPotatoes, Peas, Avocado), Heavy(Kalo, Chicken, Ddodo)<br>'
            '<br>'
            ' **Dinner:** Poa(Matooke, Gnuts Paste, Spinach), Color(Pumpkin, Beans, Bugga), <br>Rola(1 Chapati, 2 eggs, Avocado)<br>'
            '<br>'  
            '**Snacks:** Fruits(Fruits(Bananas, Half Mango, Apple, Orange ), Boiled eggs, <br>Roasted Gnuts/Soya/Simsim, Plain Yorgurt)<br>',unsafe_allow_html=True)


# Convert local image to base64
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_base64 = get_base64_image("diet.jpg")  # ← put your image file here

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
