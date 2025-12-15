# Home.py  (main app)
import streamlit as st
import numpy as np
import joblib


col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("sukaali.png", width=500)

#st.image("sukaali.png", width=450)
st.set_page_config(page_title="SukaaliCheck", layout="centered")
st.sidebar.image("type2.png")
st.sidebar.title("About Diabetes")
st.sidebar.markdown('<a href="https://idf.org/our-network/regions-and-members/africa/members/uganda/" target="_blank">Diabetes in Uganda</a>',
            unsafe_allow_html=True)
st.sidebar.markdown('<a href="https://makir.mak.ac.ug/items/6b129844-bd56-4a05-81f8-7e1b3996a9e5" target="_blank">Diabetes Risk Factors</a>',
            unsafe_allow_html=True)
st.sidebar.image("main.png")


st.sidebar.write('**Contact Us:**<br>'
                 '**hellennakabuye23@gmail.com**', unsafe_allow_html=True)

st.title("🩺Type II Diabetes Risk Predictor")
st.write("Enter the details below to estimate your risk of diabetes.")

# ---------------- INPUT FIELDS ----------------
age = st.number_input("Age", min_value=1, max_value=100, value=35)

sex = st.selectbox("Sex", ["Male", "Female"])

bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0)

physical_activity = st.selectbox(
    "Physical Activity Level",
    ["Low", "Moderate", "High"]
)

family_history = st.selectbox(
    "Family History of Diabetes",
    ["No", "Yes"]
)

hypertension = st.selectbox(
    "Hypertension",
    ["No", "Yes"]
)

diet_score = st.slider(
    "Diet Quality Score (0 = Poor, 10 = Excellent)",
    0, 10, 5
)

blood_glucose = st.number_input(
    "Fasting Blood Glucose (mg/dL)",
    min_value=50.0, max_value=300.0, value=100.0
)

st.markdown("---")

# ---------------- LOAD YOUR MODEL ----------------
@st.cache_resource
def load_model():
    return joblib.load("diabetesRF.pkl")

model = load_model()

# ---------------- ENCODERS ----------------
def encode_inputs():
    sex_encoded = 1 if sex == "Male" else 0
    fh_encoded = 1 if family_history == "Yes" else 0
    ht_encoded = 1 if hypertension == "Yes" else 0

    if physical_activity == "Low":
        pa_encoded = 0
    elif physical_activity == "Moderate":
        pa_encoded = 1
    else:  # High
        pa_encoded = 2

    return [
        age,
        sex_encoded,
        bmi,
        pa_encoded,
        fh_encoded,
        ht_encoded,
        diet_score,
        blood_glucose
    ]

risk_map = {0: "Low", 1: "Intermediate", 2: "High"}

# ---------------- PREDICT BUTTON ----------------
if st.button("Predict Diabetes Risk"):

    features = encode_inputs()

    prediction = model.predict([features])[0]
    result = risk_map.get(prediction, "Unknown")

    # ---------------- OUTPUT ----------------
    if result == "Low":
        st.success("🟢 **Low Diabetes Risk**")
        #st.write("Thank you for using SukaaliCheck!")
    elif result == "Intermediate":
        st.warning("🟡 **Intermediate Diabetes Risk**")
        #st.write("Thank you for using SukaaliCheck!")
    else:
        st.error("🔴 **High Diabetes Risk**")
        #st.write("Thank you for using SukaaliCheck!")


st.markdown(
    "<h1 style='color: green; font-style: italic; text-align: center;'>"
    "Thank YOU for Using SukaaliCheck!"
    "</h1>",
    unsafe_allow_html=True
)
