
# Insurance Premium Prediction API using FastAPI

from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
from fastapi.responses import JSONResponse
from pathlib import Path
import pickle
import pandas as pd

# Load the trained ML model
MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


# Tier 1 and Tier 2 cities
tier1_cities = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Kolkata",
    "Chennai", "Pune", "Ahmedabad", "Surat", "Jaipur"
]

tier2_cities = [
    "Lucknow", "Nagpur", "Indore", "Bhopal", "Kanpur",
    "Agra", "Varanasi", "Allahabad", "Meerut", "Ghaziabad"
]


app = FastAPI(
    title="Insurance Premium Prediction API",
    description="Predict insurance premiums using a trained ML model",
    version="1.0.0"
)


# Validation model for user input
class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120)]
    weight: Annotated[float, Field(..., gt=0)]
    height: Annotated[float, Field(..., gt=0)]
    smoker: Literal["Yes", "No"]
    income_lpa: Annotated[float, Field(..., gt=0)]
    city: str
    occupation: Literal[
        "retired",
        "freelancer",
        "student",
        "government_job",
        "unemployed",
        "business_owner",
        "private_job"
    ]

    # Calculate BMI using height in centimeters and weight in kilograms
    @computed_field
    @property
    def bmi(self) -> float:
        height_in_meters = self.height / 100
        return round(self.weight / (height_in_meters ** 2), 2)

    # Determine lifestyle risk
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker == "Yes" and self.bmi > 30:
            return "high"
        elif self.smoker == "Yes":
            return "medium"
        elif self.bmi > 30:
            return "medium"
        return "low"

    # Classify the user by age
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"


    # Determine the city tier
    @computed_field
    @property
    def city_tier(self) -> int:
        normalized_city = self.city.strip().title()

        if normalized_city in tier1_cities:
            return 1
        elif normalized_city in tier2_cities:
            return 2
        return 3


# Endpoint for predicting the insurance premium
@app.post("/predict")
def predict_premium(data: UserInput):

    # Create a DataFrame with the features expected by the ML model
    input_df = pd.DataFrame([{
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }])

    # Generate the prediction
    prediction = model.predict(input_df)[0]

    return JSONResponse(
        content={"predicted_premium": prediction},
        status_code=200
    )
