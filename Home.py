# Home.py  (main app)
import streamlit as st
import joblib
import pandas as pd
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
from reportlab.platypus import Image



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
    return joblib.load("diabetesXG.pkl")

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

def generate_pdf_report(user_data, result):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # ---------------- LOGO ----------------
    try:
        logo = Image("sukaali.png", width=120, height=60)
        elements.append(logo)
        elements.append(Spacer(1, 10))
    except:
        pass  # If logo not found, continue without crashing

    # ---------------- TITLE ----------------
    elements.append(Paragraph(
        "<b>SukaaliCheck – Diabetes Risk Assessment Report</b>",
        styles["Title"]
    ))
    elements.append(Spacer(1, 12))

    # ---------------- DATE ----------------
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    elements.append(Paragraph(f"<b>Date:</b> {date_str}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # ---------------- USER DETAILS TABLE ----------------
    table_data = [
        ["Parameter", "User Value", "Reference Value"],

        ["Age", user_data["Age"], "Adult population"],
        ["Sex", user_data["Sex"], "—"],
        ["BMI", user_data["BMI"], "18.5 – 24.9 kg/m²"],
        ["Physical Activity", user_data["Physical Activity"], "Moderate – High"],
        ["Family History", user_data["Family History"], "No"],
        ["Hypertension", user_data["Hypertension"], "No"],
        ["Diet Score", user_data["Diet Score"], "≥ 7 / 10"],
        ["Fasting Blood Glucose (mg/dL)", user_data["Blood Glucose"], "70 – 99 mg/dL"],
    ]

    table = Table(table_data, colWidths=[170, 120, 170], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgreen),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # ---------------- COLOR-CODED RESULT ----------------
    if result == "Low":
        risk_color = "green"
    elif result == "Intermediate":
        risk_color = "orange"
    else:
        risk_color = "red"

    elements.append(Paragraph(
        f"<b>Predicted Diabetes Risk Level:</b> "
        f"<font color='{risk_color}' size='14'><b>{result}</b></font>",
        styles["Heading2"]
    ))

    elements.append(Spacer(1, 12))

    # ---------------- ADVICE ----------------
    advice_map = {
        "Low": "Maintain a healthy lifestyle and regular checkups.",
        "Intermediate": "Consider lifestyle improvements and medical screening.",
        "High": "Seek medical evaluation as soon as possible."
    }

    elements.append(Paragraph(
        f"<b>Health Advice:</b> {advice_map.get(result, '')}",
        styles["Normal"]
    ))

    elements.append(Spacer(1, 15))

    # ---------------- DISCLAIMER ----------------
    elements.append(Paragraph(
        "<i>Disclaimer: This report is generated by SukaaliCheck, an AI-based "
        "screening tool. It does not replace professional medical diagnosis or treatment.</i>",
        styles["Normal"]
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer

DATA_FILE = "sukaalicheck_entries.csv"
def log_user_entry(user_data, result):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "age": user_data["Age"],
        "sex": user_data["Sex"],
        "bmi": user_data["BMI"],
        "physical_activity": user_data["Physical Activity"],
        "family_history": user_data["Family History"],
        "hypertension": user_data["Hypertension"],
        "diet_score": user_data["Diet Score"],
        "blood_glucose": user_data["Blood Glucose"],
        "predicted_risk": result
    }

    df = pd.DataFrame([entry])

    if os.path.exists(DATA_FILE):
        df.to_csv(DATA_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(DATA_FILE, index=False)


# ---------------- PREDICT BUTTON ----------------
if st.button("Predict Diabetes Risk"):

    features = encode_inputs()
    prediction = model.predict([features])[0]
    result = risk_map.get(prediction, "Unknown")

    # Display result
    if result == "Low":
        st.success("🟢 **Low Diabetes Risk**")
    elif result == "Intermediate":
        st.warning("🟡 **Intermediate Diabetes Risk**")
    else:
        st.error("🔴 **High Diabetes Risk**")

    # Collect user data
    user_data = {
        "Age": age,
        "Sex": sex,
        "BMI": bmi,
        "Physical Activity": physical_activity,
        "Family History": family_history,
        "Hypertension": hypertension,
        "Diet Score": diet_score,
        "Blood Glucose": blood_glucose,
    }

    log_user_entry(user_data, result)

    # Generate PDF
    pdf = generate_pdf_report(user_data, result)

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf,
        file_name="SukaaliCheck_Diabetes_Report.pdf",
        mime="application/pdf"
    )
    log_user_entry(user_data, result)

st.write("Current directory:", os.getcwd())
st.write("Files here:", os.listdir())




