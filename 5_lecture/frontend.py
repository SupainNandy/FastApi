import requests
import streamlit as st


st.set_page_config(page_title="Insurance Premium Predictor")
st.title("Insurance Premium Predictor")
st.write("Enter your details to get an insurance premium prediction.")

api_url = st.sidebar.text_input(
    "FastAPI URL",
    value="http://127.0.0.1:8000"
).strip().rstrip("/")

occupations = [
    "retired",
    "freelancer",
    "student",
    "government_job",
    "unemployed",
    "business_owner",
    "private_job",
]

with st.form("prediction_form"):
    age = st.number_input("Age", min_value=1, max_value=119, value=30)
    weight = st.number_input("Weight (kg)", min_value=1.0, value=70.0)
    height = st.number_input("Height (cm)", min_value=1.0, value=170.0)
    smoker = st.selectbox("Do you smoke?", options=["No", "Yes"])
    income_lpa = st.number_input(
        "Annual income (lakhs)",
        min_value=0.1,
        value=10.0,
        step=0.5,
    )
    city = st.text_input("City", value="Mumbai")
    occupation = st.selectbox("Occupation", options=occupations)
    submitted = st.form_submit_button("Predict premium")

if submitted:
    if not api_url:
        st.error("Enter the URL of the FastAPI server in the sidebar.")
    else:
        payload = {
            "age": age,
            "weight": weight,
            "height": height,
            "smoker": smoker,
            "income_lpa": income_lpa,
            "city": city.strip(),
            "occupation": occupation,
        }

        try:
            response = requests.post(
                f"{api_url}/predict",
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            st.error(
                f"Could not get a prediction from the API: {exc}. "
                "Check that FastAPI is running and the URL is correct."
            )
        else:
            try:
                result = response.json()
            except ValueError:
                st.error("The API returned a response that was not valid JSON.")
            else:
                if "predicted_premium" not in result:
                    st.error("The API response did not contain a prediction.")
                else:
                    st.success(
                        f"Predicted premium: {result['predicted_premium']}"
                    )
