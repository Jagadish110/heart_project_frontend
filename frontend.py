import streamlit as st
import requests

# Base URL of your FastAPI backend
API_URL = "https://heart-project-backend-1.onrender.com"


# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# ------------------- Register Page -------------------
def register():
    st.title("Register")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        payload = {
            "username": username,
            "email": email,
            "password": password
        }
        res = requests.post(f"{API_URL}/register", json=payload)
        if res.status_code == 200:
            st.success(res.json()["message"])
        else:
            st.error(res.json()["detail"])

# ------------------- Login Page -------------------
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        payload = {
            "username": username,
            "password": password
        }
        res = requests.post(f"{API_URL}/login", json=payload)
        if res.status_code == 200:
            data = res.json()
            st.success("Login successful")
            st.session_state.logged_in = True
            st.session_state.user_id = data["user_id"]
        else:
            st.error("Invalid credentials")

# ------------------- Prediction Page -------------------
def prediction_page():
    st.markdown(
        """
        <h2 style='text-align: center;color:#4AC6D2'>Heart Disease Prediction</h2>
        <p style='text-align:None;'>Enter your details below to predict the risk of heart disease.</p>
        """,
        unsafe_allow_html=True

    )
    age = st.number_input("Age", 1, 120,value=None)
    sex = st.selectbox("Sex", [0, 1], format_func=lambda x: "Female" if x == 0 else "Male")  # 0 = female, 1 = male
    cp = st.selectbox("Chest Pain Type (0–3)", [0, 1, 2, 3])
    trestbps = st.number_input("Resting Blood Pressure", 80, 200)
    chol = st.number_input("Cholesterol", 100, 600)
    fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1])
    restecg = st.selectbox("Resting ECG Results (0–2)", [0, 1, 2])
    thalach = st.number_input("Max Heart Rate Achieved", 60, 250)
    exang = st.selectbox("Chest Pain During Exercise", [0, 1])
    oldpeak = st.number_input("ST Depression", 0.0, 6.0)
    slope = st.selectbox("Slope of ST Segment", [0, 1, 2])

    if st.button("Predict"):
        input_data = {
            "user_id": st.session_state.user_id,
            "age": age,
            "sex": sex,
            "cp": cp,
            "trestbps": trestbps,
            "chol": chol,
            "fbs": fbs,
            "restecg": restecg,
            "thalach": thalach,
            "exang": exang,
            "oldpeak": oldpeak,
            "slope": slope
        }
        res = requests.post(f"{API_URL}/predict", json=input_data)
        if res.status_code == 200:
            result = res.json()["prediction"]
            st.success(f"Prediction: {'No Risk of Heart Disease Detected' if result == 1 else 'High Risk of Heart Disease Detected'}")
        else:
            st.error("Prediction failed.")

# ------------------- Page Routing -------------------
st.sidebar.title("Navigation")
if st.session_state.logged_in:
    choice = st.sidebar.selectbox("Menu", ["Predict", "Logout"])
else:
    choice = st.sidebar.selectbox("Menu", ["Login", "Register"])

if choice == "Login":
    if not st.session_state.logged_in:
        login()
elif choice == "Register":
    register()
elif choice == "Predict":
    if st.session_state.logged_in:
        prediction_page()
    else:
        st.warning("Please login to access prediction.")
elif choice == "Logout":
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.success("Logged out successfully.")
