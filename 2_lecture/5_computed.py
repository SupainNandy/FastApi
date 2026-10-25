# Computed Validation in Pydantic allows you to define fields that are derived from other fields in your model. This is useful when you want to calculate a value based on the input data, rather than having the user provide it directly.
from pydantic import BaseModel, Field, EmailStr, model_validator, computed_field
from typing import List, Dict

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float #kg
    height: float #meter
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def calculate_bmi(self)-> float:
        # BMI = weight (kg) / (height (m))^2
        return  round(self.weight / (self.height ** 2)/ 2)



def update_patient(patient: Patient):
    print("Updating patient data...")
    print("Name:", patient.name)
    print("Email:", patient.email)
    print("Age:", patient.age)
    print("Weight:", patient.weight)
    print("Height:", patient.height)
    print("Married:", patient.married)
    print("Allergies:", patient.allergies)
    print("Contact Details:", patient.contact_details)
    print("BMI:", patient.calculate_bmi)

patient_data = {
    "name": "John Doe",
    "email": "jhon@gmail.com",
    "age": 67,
    "weight": 70.5,
    "height": 1.75, 
    "married": True,
    "allergies": ["pollen", "dust"],
    "contact_details": {
        "phone": "1234567890",
        "address": "123 Main St",
        "emergency": "9876543210"  # Emergency contact provided
    }
}

patient1 = Patient(**patient_data)

update_patient(patient1)

