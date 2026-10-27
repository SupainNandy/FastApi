
from typing import Annotated, Literal
import json
from pathlib import Path as FilePath

from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field, computed_field


# Pydantic model for validating patient data
class Patient(BaseModel):
    id: Annotated[int, Field(..., description="Unique patient identifier")]
    name: Annotated[str, Field(..., description="Name of the patient")]
    email: Annotated[EmailStr, Field(..., description="Valid email address")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age between 1 and 119")]
    height: Annotated[float, Field(..., gt=0, description="Height in centimeters")]
    weight: Annotated[float, Field(..., gt=0, description="Weight in kilograms")]
    gender: Annotated[
        Literal["Male", "Female", "Other"],
        Field(..., description="Gender of the patient")
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        # Convert height from centimeters to meters and calculate BMI.
        height_in_meters = self.height / 100
        return round(self.weight / (height_in_meters ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        # Categorize BMI using standard adult BMI thresholds.
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal weight"
        elif self.bmi < 30:
            return "Overweight"
        return "Obese"


app = FastAPI(
    title="My First FastAPI",
    description="My first Python API",
    version="1.0.0"
)


# Read patient records from patient.json.
def load_data():
    file_path = FilePath(__file__).resolve().parent / "patient.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# Save patient records to patient.json.
def save_data(data):
    file_path = FilePath(__file__).resolve().parent / "patient.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


@app.get("/")
def home():
    return {"message": "FastAPI is running!"}


@app.get("/about")
def about():
    return {"project": "FastAPI", "status": "success"}


@app.get("/patient")
def fetch_data():
    return load_data()


# Fetch a patient using a path parameter.
@app.get("/patient/{pid}")
def fetch_patient_by_id(
    pid: Annotated[int, Path(..., description="Patient ID")]
):
    patients = load_data()

    for patient in patients:
        if patient["id"] == pid:
            return patient

    raise HTTPException(status_code=404, detail="Patient not found")


# Sort patients using query parameters.
@app.get("/sort")
def sort_patients(
    sort_by: Annotated[
        str, Query(..., description="Sort by height, weight, or bmi")
    ],
    order: Annotated[
        str, Query(description="Sort order: asc or desc")
    ] = "asc",
):
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field; select from {valid_fields}"
        )

    order = order.lower()

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order; select asc or desc"
        )

    patients = load_data()

    # Calculate BMI dynamically so older JSON records work too.
    def get_sort_value(patient):
        if sort_by == "bmi":
            height_m = patient["height"] / 100
            return patient["weight"] / (height_m ** 2)

        return patient[sort_by]

    return sorted(
        patients,
        key=get_sort_value,
        reverse=(order == "desc")
    )


# Create a new patient.
@app.post("/create", status_code=201)
def create_patient(patient: Patient):
    patients = load_data()

    # Prevent duplicate patient IDs.
    for existing_patient in patients:
        if existing_patient["id"] == patient.id:
            raise HTTPException(
                status_code=400,
                detail="Patient with this ID already exists"
            )

    # model_dump() includes the computed BMI and verdict fields.
    patients.append(patient.model_dump())

    save_data(patients)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Patient created successfully",
            "patient": patient.model_dump()
        }
    )
