
# ============================================================
# 1. INSTALL REQUIRED PACKAGES
# ============================================================

# Install Pydantic:
# python3 -m pip install "pydantic"

# Install Pydantic with email validation support:
# python3 -m pip install "pydantic[email]"


# ============================================================
# 2. IMPORT REQUIRED MODULES
# ============================================================

from pydantic import BaseModel, EmailStr, AnyUrl, Field

# BaseModel: Creates a model for data validation.
# EmailStr: Checks whether an email address has a valid format.
# AnyUrl: Checks whether a URL has a valid format.
# Field: Adds validation rules and extra information to fields.

from typing import List, Dict, Optional, Annotated

# List: Defines a list of values.
# Dict: Defines a dictionary with keys and values.
# Optional: Allows a field to contain None.
# Annotated: Adds extra validation rules or information to a type.


# ============================================================
# 3. CREATE THE PATIENT MODEL
# ============================================================

class Patient(BaseModel):

    # Name must be a string.
    # The name cannot contain more than 50 characters.
    # Field also provides extra information about the name.
    name: Annotated[
        str,
        Field(
            max_length=50,
            title='Name of the patient',
            description='Enter patient name under 50 characters',
            examples=['Nitish', 'Amit']
        )
    ]

    # EmailStr checks the email format.
    email: EmailStr

    # AnyUrl checks the URL format.
    linkedin_url: AnyUrl

    # Age must be greater than 0 and less than 120.
    age: int = Field(gt=0, lt=120)

    # Weight must be greater than 0.
    # strict=True prevents automatic type conversion.
    # For example, the string "50.2" will not be accepted as a float.
    weight: Annotated[float, Field(gt=0, strict=True)]

    # If married is not provided, its default value is False.
    married: bool = Annotated[bool, Field(default=None)]

    # Allergies can contain a list of strings.
    # The list can contain a maximum of 5 items.
    # If allergies is not provided, its value will be None.
    allergies: Annotated[
        Optional[List[str]],
        Field(default=None, max_length=5)
    ]

    # Contact details can contain a dictionary.
    # Both dictionary keys and values must be strings.
    # If contact details are not provided, the value will be None.
    contact_details: Optional[Dict[str, str]] = None


# ============================================================
# 4. CREATE PATIENT DATA
# ============================================================

patient_info = {
    "name": "Nitesh",
    "email": "abc@gmail.com",
    "linkedin_url": "http://linkedin.com/123",
    "age": 22,
    "weight": 50.2,

    # We can also provide these optional fields:
    # "married": True,
    # "allergies": ["pollen", "dust"],
    # "contact_details": {
    #     "email": "abc@gmail.com",
    #     "phone": "2345678899"
    # }
}


# ============================================================
# 5. VALIDATE DATA AND CREATE AN OBJECT
# ============================================================

# ** unpacks the dictionary into keyword arguments.
# Pydantic checks the provided data against the Patient model.
# If the data is invalid, Pydantic raises a validation error.
patient1 = Patient(**patient_info)


# ============================================================
# 6. CREATE THE INSERT FUNCTION
# ============================================================

def insert_patient_data(patient: Patient):

    # Print the patient's information.
    # The function expects a Patient object.
    print("Name: ", patient.name)
    print("LinkedIn URL: ", patient.linkedin_url)
    print("Email: ", patient.email)
    print("Age: ", patient.age)
    print("Married: ", patient.married)

    # Print a success message.
    # This does not actually insert data into a database.
    print("Patient data inserted successfully.")


# ============================================================
# 7. CREATE THE UPDATE FUNCTION
# ============================================================

def update_patient_data(patient: Patient):

    # Print the patient's name and age.
    print("Name: ", patient.name)
    print("Age: ", patient.age)

    # Print the patient's weight.
    # Pydantic validates the weight when the object is created.
    print("Weight: ", patient.weight)

    # Print the allergy list and contact details.
    print("Allergies: ", patient.allergies)
    print("Contact Details: ", patient.contact_details)

    # Print a success message.
    # This does not actually update a database.
    print("Patient data updated successfully.")


# ============================================================
# 8. CALL THE FUNCTIONS
# ============================================================

# Pass the Patient object to the insert function.
insert_patient_data(patient1)

# Pass the same Patient object to the update function.
update_patient_data(patient1)
