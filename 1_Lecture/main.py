
from fastapi import FastAPI, HTTPException, Path as FastAPIPath
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

@app.get("/patient/{pid}")
def fetch_patient_by_id(pid: int = FastAPIPath(..., description='Id of the patient in the db', example='1')):
    patients = load_data()
    for patient in patients:
        if patient["id"] == pid:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")
