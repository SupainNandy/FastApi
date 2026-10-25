
"""
Pydantic Field Validator Tutorial

Topics covered:
1. Creating a Pydantic model
2. Email validation
3. Data transformation
4. Age validation using mode='before'
5. Creating and using a Patient object
"""

# ============================================================
# STEP 1: IMPORT REQUIRED MODULES
# ============================================================

from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Dict


# ============================================================
# STEP 2: CREATE THE PATIENT MODEL
# ============================================================

class Patient(BaseModel):
    # Patient name must be a string.
    name: str

    # EmailStr checks whether the email format is valid.
    email: EmailStr

    # Patient age must be an integer.
    age: int

    # Patient weight must be a number.
    weight: float

    # Married must be True or False.
    married: bool

    # Allergies must be a list of strings.
    # Example: ["pollen", "dust"]
    allergies: List[str]

    # Contact details must be a dictionary
    # containing string keys and string values.
    # Example: {"phone": "25637849"}
    contact_details: Dict[str, str]


    # ========================================================
    # STEP 3: VALIDATE THE EMAIL FIELD
    # ========================================================

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):

        # Only these email domains are allowed.
        valid_domain = ['hdfc.com', 'icici.com']

        # Extract the domain from the email.
        # Example: abc@hdfc.com -> hdfc.com
        domain_name = value.split('@')[-1]

        # Reject the email if its domain is not allowed.
        if domain_name not in valid_domain:
            raise ValueError(
                'Email domain must be hdfc.com or icici.com'
            )

        # Return the email if validation succeeds.
        return value


    # ========================================================
    # STEP 4: TRANSFORM THE PATIENT NAME
    # ========================================================

    @field_validator('name')
    @classmethod
    def transform_name(cls, value):

        # Convert the name into uppercase.
        # Example: nitesh -> NITESH
        return value.upper()


    # ========================================================
    # STEP 5: VALIDATE AGE BEFORE TYPE PARSING
    # ========================================================

    @field_validator('age', mode='before')
    @classmethod
    def validateAge(cls, value):

        # Check that the input is an integer before
        # comparing it with the age limits.
        # bool is excluded because True and False are
        # subclasses of int in Python.
        if type(value) is not int:
            raise ValueError('Age must be an integer')

        # Age must be greater than 0 and less than 100.
        if 0 < value < 100:
            return value

        # Reject ages outside the allowed range.
        raise ValueError('Age should be between 1 and 99')


# ============================================================
# STEP 6: CREATE A FUNCTION TO DISPLAY PATIENT DATA
# ============================================================

def update_Patient(patient: Patient):

    # Access values from the Patient object.
    print("Name:", patient.name)
    print("Email:", patient.email)
    print("Age:", patient.age)
    print("Weight:", patient.weight)
    print("Married:", patient.married)
    print("Allergies:", patient.allergies)
    print("Contact Details:", patient.contact_details)

    print("Patient data displayed successfully.")


# ============================================================
# STEP 7: CREATE PATIENT DATA
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
# STEP 8: VALIDATE DATA AND CREATE A PATIENT OBJECT
# ============================================================

# ** unpacks the dictionary into keyword arguments.
# Pydantic validates the fields and runs the validators.
# If validation fails, a ValidationError is raised.
patient1 = Patient(**patient_info)


# ============================================================
# STEP 9: CALL THE FUNCTION
# ============================================================

# Pass the validated Patient object to the function.
update_Patient(patient1)
