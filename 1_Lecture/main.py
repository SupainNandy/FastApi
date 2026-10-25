
from fastapi import FastAPI, HTTPException, Path, Query
import json
from pathlib import Path as FilePath

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

