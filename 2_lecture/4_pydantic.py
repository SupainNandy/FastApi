
# Model Validation with Pydantic

from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Dict


# Step 1: Create the Patient model
class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    # Step 2: Validate multiple fields together
    @model_validator(mode='after')
    def validate_emergency_contact(self):

        # Patients over 60 must provide an emergency contact.
        if (
            self.age > 60
            and 'emergency' not in self.contact_details
        ):
            raise ValueError(
                "Emergency contact is required for patients over 60."
            )

        # Return the validated Patient object.
        return self


# Step 3: Create patient data
patient_data = {
    "name": "John Doe",
    "email": "jhon@gmail.com",
    "age": 67,
    "weight": 70.5,
    "married": True,
    "allergies": ["pollen", "dust"],
    "contact_details": {
        "phone": "1234567890",
        "address": "123 Main St",
        "emergency": "9876543210"  # Emergency contact provided
    }
    
}


# Step 4: Validate data and create a Patient object
patient1 = Patient(**patient_data)


# Step 5: Display patient information
def update_patient(patient: Patient):
    print("Updating patient data...")
    print("Name:", patient.name)
    print("Email:", patient.email)
    print("Age:", patient.age)
    print("Weight:", patient.weight)
    print("Married:", patient.married)
    print("Allergies:", patient.allergies)
    print("Contact Details:", patient.contact_details)
    print("Patient data updated successfully.")


# Step 6: Call the function
update_patient(patient1)
