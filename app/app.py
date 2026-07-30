# Import libraries
import streamlit as st
import pandas as pd
import joblib

# Load saved model
model = joblib.load('xgb_cvd_model_tuned.pkl')

# App title
st.set_page_config(page_title="CVD Risk Prediction", layout="centered")
st.title("💖 Cardiovascular Disease (CVD) Risk Prediction App")
st.markdown("---")

# Sidebar for user inputs
with st.sidebar:
    st.header("🔍 Enter Patient Information")
    st.write("Please fill out the patient's details below for CVD risk prediction:")

    age_years = st.number_input("🧓 Age (years)", min_value=1, max_value=120, value=30)
    gender = st.selectbox("🚻 Gender", ["Female (1)", "Male (2)"])
    height = st.number_input("📏 Height (cm)", min_value=100, max_value=250, value=170)
    weight = st.number_input("⚖️ Weight (kg)", min_value=30, max_value=200, value=70)

    st.markdown("### 🩺 Blood Pressure Details")
    ap_hi = st.number_input("Systolic Blood Pressure (ap_hi)", min_value=80, max_value=250, value=120)
    ap_lo = st.number_input("Diastolic Blood Pressure (ap_lo)", min_value=40, max_value=150, value=80)

    st.markdown("### 🧬 Health and Lifestyle")
    cholesterol = st.selectbox("Cholesterol Level", ["Normal (1)", "Above Normal (2)", "Well Above Normal (3)"])
    gluc = st.selectbox("Glucose Level", ["Normal (1)", "Above Normal (2)", "Well Above Normal (3)"])
    smoke = st.selectbox("Do you smoke?", ["No (0)", "Yes (1)"])
    alco = st.selectbox("Do you consume alcohol?", ["No (0)", "Yes (1)"])
    active = st.selectbox("Are you physically active?", ["No (0)", "Yes (1)"])

# Converting text selections to numbers (fixed safely!)
gender = 1 if gender == "Female (1)" else 2

cholesterol_mapping = {
    "Normal (1)": 1,
    "Above Normal (2)": 2,
    "Well Above Normal (3)": 3
}
cholesterol = cholesterol_mapping[cholesterol]

gluc_mapping = {
    "Normal (1)": 1,
    "Above Normal (2)": 2,
    "Well Above Normal (3)": 3
}
gluc = gluc_mapping[gluc]

smoke_mapping = {
    "No (0)": 0,
    "Yes (1)": 1
}
smoke = smoke_mapping[smoke]
alco = smoke_mapping[alco]
active = smoke_mapping[active]

# Calculate extra features
age = age_years * 365
BMI = weight / ((height / 100) ** 2)

# Create input dataframe
input_data = pd.DataFrame([{
    'age': age,
    'gender': gender,
    'height': height,
    'weight': weight,
    'ap_hi': ap_hi,
    'ap_lo': ap_lo,
    'cholesterol': cholesterol,
    'gluc': gluc,
    'smoke': smoke,
    'alco': alco,
    'active': active,
    'age_years': age_years,
    'BMI': BMI
}])

# Main panel
st.subheader("📝 Patient Summary")
st.dataframe(input_data)

# Prediction button
if st.button("🚀 Predict CVD Risk"):
    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)[0][1]

    st.markdown("---")
    if prediction[0] == 1:
        st.error(f"🔴 **Prediction Outcome:**\n\nThe patient is **likely at risk** for Cardiovascular Disease.\n\n🧪 **Estimated Risk Probability:** {probability:.2%}\n\nℹ️ *Note: Further medical examination is recommended for accurate clinical assessment.*")
    else:
        st.success(f"🟢 **Prediction Outcome:**\n\nThe patient is **unlikely to have** Cardiovascular Disease.\n\n🧪 **Estimated Risk Probability:** {probability:.2%}\n\nℹ️ *Note: This prediction is based on the model's analysis and should not replace professional medical diagnosis.*")
