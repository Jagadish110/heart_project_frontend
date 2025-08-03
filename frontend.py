import streamlit as st
import requests

API_URL = "https://heart-project-backend-3.onrender.com"

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# ------------------- Register Page -------------------
def register():
    st.title("Register")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        # Check for blank fields
        if not username or not email or not password:
            st.error("Please fill in all fields!")
            return

        payload = {
            "username": username,
            "email": email,
            "password": password
        }
        try:
            res = requests.post(f"{API_URL}/register", json=payload)
            if res.status_code == 200:
                st.success(res.json().get("message", "Registration successful!"))
            else:
                try:
                    err = res.json()
                    # Show all error keys for easier debugging
                    if "detail" in err:
                        st.error(err["detail"])
                    else:
                        st.error(str(err))
                except Exception as e:
                    st.error(f"Registration failed. Raw response: {res.text}")
        except Exception as e:
            st.error(f"Connection error: {e}")


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
            st.session_state.username = username  # Set the username in session!
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
    age = st.number_input("Age", 1, 120, value=None)
    sex = st.selectbox("Sex", [0, 1], format_func=lambda x: "Female" if x == 0 else "Male")
    Chest_Pain = st.selectbox("Chest Pain Type (0–3)", [0, 1, 2, 3],format_func=lambda x:["Typical Angina","AtypicalAngina","Non-anginal pain","Asymptomatic"][x])
    Resting_Blood_Pressure = st.number_input("Resting Blood Pressure", 80, 200, value=None)
    Cholesterol = st.number_input("Cholesterol", 100, 600, value=None)
    Fasting_Blood_Sugar = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1],format_func=lambda x:"No" if x==0 else "Yes")
    Resting_ECG_Results = st.selectbox("Resting ECG Results (0–2)", [0,1,2],format_func=lambda x: ["Normal","ST-T wave abnormality","Left ventricular hypertrophy"][x])
    Maximum_Heart_Rate_Achieved = st.number_input("Max Heart Rate Achieved", 60, 250, value=None)
    Chest_Pain_During_Exercise = st.selectbox("Chest Pain During Exercise", [0, 1],format_func=lambda x:"No" if x==0 else "Yes")
    ST_depression_level = st.number_input("ST Depression", 0.0, 6.0, value=None)
    Slope_of_ST_segment = st.selectbox("Slope of ST Segment", [0,1,2],format_func=lambda x:["Unsloping","Flat","Downsloping"][x])

    if st.button("Predict"):
        input_data = {
            "username": st.session_state.username,  # Correct session key!
            "age": age,
            "sex": sex,
            "Chest_Pain": Chest_Pain,
            "Resting_Blood_Pressure": Resting_Blood_Pressure,
            "Cholesterol": Cholesterol,
            "Fasting_Blood_Sugar": Fasting_Blood_Sugar,
            "Resting_ECG_Results": Resting_ECG_Results,
            "Maximum_Heart_Rate_Achieved": Maximum_Heart_Rate_Achieved,
            "Chest_Pain_During_Exercise": Chest_Pain_During_Exercise,
            "ST_depression_level": ST_depression_level,
            "Slope_of_ST_segment": Slope_of_ST_segment
        }
        res = requests.post(f"{API_URL}/predict", json=input_data)
        if res.status_code == 200:
            result = res.json()["prediction"]
            st.success(f"Prediction: {'No Risk of Heart Disease Detected' if result == 1 else 'High Risk of Heart Disease Detected'}")
        else:
            st.error("Prediction failed, make sure you are logged in and have filled all fields.")

# ------------------- Page Routing -------------------
st.sidebar.title("Navigation")

# Single menu with all options
choice = st.sidebar.selectbox("Menu", ["Login", "Register", "Predict", "Logout"])

# Logic based on selected choice
if choice == "Login":
    if not st.session_state.get("logged_in", False):
        login()
    else:
        st.info("You're already logged in.")

elif choice == "Register":
    register()

elif choice == "Predict":
    if st.session_state.get("logged_in", False):
        prediction_page()
    else:
        st.warning("Please login to access the prediction page.")

elif choice == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = None
    st.success("Logged out successfully.")


