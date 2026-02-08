import streamlit as st
import joblib
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# ---------------- PAGE CONFIG (MUST BE FIRST) ----------------
st.set_page_config(page_title="SukaaliCheck", layout="centered")

# ---------------- HEADER ----------------
# Load image
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("sukaali.png", width=500)

st.markdown(
    "<div style='text-align:center; font-size:18px; color:#333; font-weight: bold; font-style: italic;'>"
    "Predict your Type II Diabetes Risk in Seconds"
    "</div>",
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
st.sidebar.image("type2.png")
st.sidebar.title("📖 About Diabetes")

st.sidebar.markdown(
    "Diabetes is a chronic disease that occurs when the body cannot properly process glucose."
)

st.sidebar.markdown("### 🌐 Useful Links")
st.sidebar.markdown(
    '<a href="https://idf.org/our-network/regions-and-members/africa/members/uganda/" target="_blank">Diabetes in Uganda</a><br>'
    '<a href="https://makir.mak.ac.ug/items/6b129844-bd56-4a05-81f8-7e1b3996a9e5" target="_blank">Diabetes Risk Factors</a>',
    unsafe_allow_html=True
)

# st.sidebar.image("main.png")
st.sidebar.markdown("### 📧 Contact")
st.sidebar.markdown('<a href="mailto:hellennakabuye23@gmail.com">hellennakabuye23@gmail.com</a>', unsafe_allow_html=True)

# ---------------- MAIN TITLE ----------------
st.title("🩺 Type II Diabetes Risk Predictor")
#st.write("Enter the details below to estimate your risk of diabetes.")

st.markdown(
    '<div style="background-color:#e6f2ff; padding:10px; border-radius:5px;">'
    'Enter your details below to estimate your Type II Diabetes risk.'
    '</div>',
    unsafe_allow_html=True
)

# ---------------- LANGUAGE SUPPORT ----------------
# ---------------- LANGUAGE SUPPORT ----------------
language = st.selectbox(
    "Language / Olulimi",
    ["English", "Luganda"]
)

TEXT = {
    "English": {
        "tagline": "Predict your Type II Diabetes Risk in Seconds",
        "intro": "Enter your details below to estimate your Type II Diabetes risk.",

        "age": "Age",
        "sex": "Sex",
        "male": "Male",
        "female": "Female",
        "bmi": "BMI",
        "pa": "Physical Activity Level",
        "fh": "Family History of Diabetes",
        "ht": "Hypertension",
        "diet": "Diet Quality Score (0 = Poor, 10 = Excellent)",
        "glucose": "Fasting Blood Glucose (mg/dL)",

        "predict": "Predict Diabetes Risk",
        "download": "📄 Download Your Diabetes Risk Report",

        "low": "🟢 Low Diabetes Risk",
        "intermediate": "🟡 Intermediate Diabetes Risk",
        "high": "🔴 High Diabetes Risk",

        "low_msg": "Maintain healthy lifestyle and regular checkups.",
        "int_msg": "Consider lifestyle improvements and medical screening.",
        "high_msg": "Seek medical evaluation as soon as possible."
    },

    "Luganda": {
        "tagline": "Kebera Obulabe bwa Sukaali mu Biseera Bitono",
        "intro": "Yingiza ebikwata ku bulamu bwo okukebera obulabe bwa Sukaali.",

        "age": "Emyaka",
        "sex": "Obutonde",
        "male": "Omusajja",
        "female": "Omukazi",
        "bmi": "Obuzito Ku Buwanvu (BMI)",
        "pa": "Omuwendo gwa Dduyiro",
        "fh": "Obulwadde bwa Sukaali mu Kika",
        "ht": "Puleesa",
        "diet": "Endya yo (0 = Mbi, 10 = Nnungi)",
        "glucose": "Sukaali mu Musaayi(mg/dL)",

        "predict": "Kebera Obulabe bwa Sukaali",
        "download": "📄 Funa Lipoota yo eya Sukaali",

        "low": "🟢 Obulabe Butono",
        "intermediate": "🟡 Obulabe wakati",
        "high": "🔴 Obulabe Bungi",

        "low_msg": "Genda mu maaso n'obulamu obulungi n'okwekebeera bulijjo.",
        "int_msg": "Kyetaagisa okukyusa ku mpisa z'obulamu n'okukebeerwa kw'omusawo.",
        "high_msg": "Kyetaagisa okulaba omusawo mangu ddala."
    }
}

t = TEXT[language]

# ---------------- INPUT FIELDS ----------------

# ---------------- INPUT FIELDS ----------------
col1, col2 = st.columns(2)

with col1:
    age = st.number_input(t["age"], min_value=1, max_value=100, value=35)
    sex = st.selectbox(t["sex"], [t["male"], t["female"]])

with col2:
    bmi = st.number_input(t["bmi"], min_value=10.0, max_value=60.0, value=25.0)
    physical_activity = st.selectbox(
        t["pa"], ["Low", "Moderate", "High"]
    )

family_history = st.selectbox(
    t["fh"], ["No", "Yes"]
)

hypertension = st.selectbox(
    t["ht"], ["No", "Yes"]
)

diet_score = st.slider(
    t["diet"], 0, 10, 5
)

blood_glucose = st.number_input(
    t["glucose"], min_value=50.0, max_value=300.0, value=100.0
)

st.markdown("---")


# ---------------- PDF GENERATION ----------------
def generate_pdf_report(user_data, result):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    try:
        logo = Image("sukaali.png", width=120, height=60)
        elements.append(logo)
        elements.append(Spacer(1, 10))
    except Exception:
        pass

    elements.append(Paragraph(
        "<b>SukaaliCheck – Diabetes Risk Assessment Report</b>",
        styles["Title"]
    ))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 12))

    table_data = [
        ["Parameter", "User Value", "Reference Value"],
        ["Age", user_data["Age"], "Adult population"],
        ["Sex", user_data["Sex"], "—"],
        ["BMI", user_data["BMI"], "18.5 – 24.9 kg/m²"],
        ["Physical Activity", user_data["Physical Activity"], "Moderate – High"],
        ["Family History", user_data["Family History"], "No"],
        ["Hypertension", user_data["Hypertension"], "No"],
        ["Diet Score", user_data["Diet Score"], "≥ 7 / 10"],
        ["Fasting Blood Glucose", user_data["Blood Glucose"], "70 – 99 mg/dL"],
    ]

    table = Table(table_data, colWidths=[170, 120, 170])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgreen),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    risk_color = {"Low": "green", "Intermediate": "orange", "High": "red"}[result]

    elements.append(Paragraph(
        f"<b>Predicted Diabetes Risk:</b> "
        f"<font color='{risk_color}' size='14'><b>{result}</b></font>",
        styles["Heading2"]
    ))

    advice = {
        "Low": t["low_msg"],
        "Intermediate": t["int_msg"],
        "High": t["high_msg"]
    }

    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"<b>Health Advice:</b> {advice[result]}", styles["Normal"]))

    elements.append(Spacer(1, 15))
    elements.append(Paragraph(
        "<i>This report is AI-generated and does not replace professional medical advice.</i>",
        styles["Normal"]
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# ---------------- GOOGLE SHEETS ----------------
if "gcp_service_account" not in st.secrets:
    st.error("Google credentials not configured.")
    st.stop()

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)
sheet = client.open("SukaaliCheck_User_Data").worksheet("data")

def save_user_input(age, sex, bmi, pa, fh, ht, diet, glucose, risk):
    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        age, sex, bmi, pa, fh, ht, diet, glucose, risk
    ])

# ---------------- PREDICTION ----------------

# ---------------- LOAD MODEL ----------------
model = joblib.load("SdiabetesRF.pkl")
feature_columns = joblib.load("feature_columns.pkl")

if st.button("Predict Diabetes Risk"):

    user_input = {
        "Age": age,
        "BMI": bmi,
        "Diet_Score": diet_score,
        "Blood_Glucose": blood_glucose,

        "Sex_Male": 1 if sex == "Male" else 0,

        "Physical_Activity_Low": 1 if physical_activity == "Low" else 0,
        "Physical_Activity_Moderate": 1 if physical_activity == "Moderate" else 0,
        "Physical_Activity_High": 1 if physical_activity == "High" else 0,

        "Family_History_Yes": 1 if family_history == "Yes" else 0,
        "Hypertension_Yes": 1 if hypertension == "Yes" else 0,
    }

    X_input = pd.DataFrame([user_input])

    # 🔥 CRITICAL LINE
    X_input = X_input.reindex(columns=feature_columns, fill_value=0)

    prediction = model.predict(X_input)[0]

    risk_map = {0: "Low", 1: "Intermediate", 2: "High"}
    result = risk_map[prediction]

    if result == "Low":
        st.success(t["low"])
        st.write(t["low_msg"])
    elif result == "Intermediate":
        st.warning(t["intermediate"])
        st.write(t["int_msg"])
    else:
        st.error(t["high"])
        st.write(t["high_msg"])

    user_data = {
        "Age": age,
        "Sex": sex,
        "BMI": bmi,
        "Physical Activity": physical_activity,
        "Family History": family_history,
        "Hypertension": hypertension,
        "Diet Score": diet_score,
        "Blood Glucose": blood_glucose
    }

    save_user_input(age, sex, bmi, physical_activity,
                    family_history, hypertension,
                    diet_score, blood_glucose, result)

    pdf = generate_pdf_report(user_data, result)

    st.download_button(
        "📄 Download Your Diabetes Risk Report",
        data=pdf,
        file_name="SukaaliCheck_Diabetes_Report.pdf",
        mime="application/pdf",
        key="download-pdf",
        use_container_width=True
    )

