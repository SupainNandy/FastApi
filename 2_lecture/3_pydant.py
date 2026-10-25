
from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Dict


# ============================================================
# STEP 1: CREATE THE PATIENT MODEL
# ============================================================

class Patient(BaseModel):
    # Patient name must be a string
    name: str

    # EmailStr checks whether the email format is valid
    email: EmailStr

    # Patient age must be an integer
    age: int

    # Patient weight must be a number
    weight: float

    # Patient marital status must be True or False
    married: bool

    # Allergies must be a list of strings
    # Example: ["pollen", "dust"]
    allergies: List[str]

    # Contact details must be a dictionary with string keys and values
    # Example: {"phone": "25637849"}
    contact_details: Dict[str, str]


    # ========================================================
    # STEP 2: VALIDATE THE EMAIL FIELD
    # ========================================================

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):

        # Only these email domains are allowed
        valid_domain = ['hdfc.com', 'icici.com']

        # Get the domain part from the email
        # Example: abc@hdfc.com -> hdfc.com
        domain_name = value.split('@')[-1]

        # Check whether the email domain is allowed
        if domain_name not in valid_domain:
            raise ValueError(
                'Email domain must be hdfc.com or icici.com'
            )

        # Return the email if validation is successful
        return value


    # ========================================================
    # STEP 3: TRANSFORM THE PATIENT NAME
    # ========================================================

    @field_validator('name')
    @classmethod
    def transform_name(cls, value):

        # Convert the patient name to uppercase
        # Example: "nitesh" -> "NITESH"
        return value.upper()


# ============================================================
# STEP 4: CREATE A FUNCTION TO DISPLAY PATIENT DATA
# ============================================================

def update_Patient(patient: Patient):

    # Access the values from the Patient object
    print("Name:", patient.name)
    print("Email:", patient.email)
    print("Age:", patient.age)
    print("Weight:", patient.weight)
    print("Married:", patient.married)
    print("Allergies:", patient.allergies)
    print("Contact Details:", patient.contact_details)

    print("Updated successfully")


# ============================================================
# STEP 5: CREATE PATIENT DATA
# ============================================================

patient_info = {
    'name': 'nitesh',
    'email': 'abc@hdfc.com',
    'age': 30,
    'weight': 75,
    'married': True,
    'allergies': ['pollen', 'dust'],
    'contact_details': {'phone': '25637849'}
}


# ============================================================
# STEP 6: VALIDATE DATA AND CREATE A PATIENT OBJECT
# ============================================================

# ** unpacks the dictionary into keyword arguments
# Pydantic checks the data types and runs the validators
patient1 = Patient(**patient_info)


# ============================================================
# STEP 7: CALL THE FUNCTION
# ============================================================

# Pass the validated Patient object to the function
update_Patient(patient1)
