
from typing import Annotated,Literal

from fastapi import FastAPI, HTTPException, Path, Query
import json
from pathlib import Path as FilePath
from pydantic import BaseModel, EmailStr, Field, computed_field

# //Pydantic model for patient data validation
class Patient(BaseModel):
    id: Annotated[int, Field(..., description="Unique identifier for the patient")]
    name: Annotated[str, Field(..., description="Name of the patient")]
    email: EmailStr = Annotated[EmailStr, Field(..., description="Email address of the patient")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient, must be a non-negative integer")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in centimeters, must be a meters")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kilograms, must be a KG")]
    gender: Annotated[Literal["Male", "Female", "Other"], Field(..., description="Gender of the patient, must be 'Male', 'Female', or 'Other'")]

    @computed_field
    @property
    def bmi(self) -> float:
        # Calculate BMI using the formula: weight (kg) / (height (m))^2
        height_in_meters = self.height / 100  # Convert height from cm to meters
        return round(self.weight / (height_in_meters ** 2), 2)  # Round to 2 decimal places
    
    @computed_field
    @property
    def verdict(self) -> str:
        # Determine the BMI category based on the calculated BMI value
        bmi_value = self.bmi
        if bmi_value < 18.5:
            return "Underweight"
        elif 18.5 <= bmi_value < 25:
            return "Normal weight"
        elif 25 <= bmi_value < 30:
            return "Overweight"
        else:
            return "Obese"

app = FastAPI(
    title="My First FastAPI",
    description="My first Python API",
    version="1.0.0"
)

# json file reading
def load_data():
    file_path = FilePath(__file__).resolve().parent / "patient.json"
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Load Data
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

#Dynamic Api params, Path parameters
@app.get("/patient/{pid}")
def fetch_patient_by_id(pid: int = Path(..., description="Id of the patient in the database")):
    patients = load_data()
    for patient in patients:
        if patient["id"] == pid:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")


#Query Parameters
@app.get('/sort')
def sort_patients(
    sort_by: str = Query(..., description="Sort by height, weight, or bmi"),
    order: str = Query("asc", description="Sort in asc or desc order"),
):

    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field; select from {valid_fields}")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order; select asc or desc")

    data = load_data()
    sorted_flag = True if order=='desc' else False

    return sorted(data, key=lambda patient: patient[sort_by], reverse=sorted_flag)



#POST endpoint to add a new patient
@app.post("/create"):
def create_patient(patient: Patient):#pydantic object 
    #load data from json file
    patients = load_data() #python dictionary

    #check if patient with same id already exists
    for existing_patient in patients:
        if existing_patient["id"] == patient.id:
            raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    #Add new patient to the list
    patients.model.dump(id=patient.id, name=patient.name, email=patient.email, age=patient.age, height=patient.height, weight=patient.weight, gender=patient.gender)

    #save into json file
    save_data(patients)
