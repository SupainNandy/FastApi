
# ============================================================
# PYDANTIC: NESTED MODEL AND model_dump()
# ============================================================

from pydantic import BaseModel, EmailStr


# ============================================================
# STEP 1: CREATE THE ADDRESS MODEL
# ============================================================

class Address(BaseModel):
    # Address is a Pydantic model used to store address details.
    # BaseModel provides automatic data validation and parsing.
    # Each field has a type annotation that defines its expected data type.

    street: str
    city: str
    state: str
    zip_code: str


# ============================================================
# STEP 2: CREATE THE PATIENT MODEL
# ============================================================

class Patient(BaseModel):
    # Patient is a Pydantic model used to store patient information.
    # EmailStr validates that the email has a valid email format.

    name: str
    email: EmailStr
    age: int

    # Default value: if gender is not provided, it will be "Male".
    gender: str = "Male"

    # NESTED MODEL:
    # Address is used as a field type inside the Patient model.
    # This allows the patient to have structured address information.
    # Pydantic validates the nested address data as well.
    address: Address


# ============================================================
# STEP 3: CREATE ADDRESS DATA
# ============================================================

# Create a Python dictionary containing address information.
# The dictionary keys must match the fields defined in Address.

address_dict = {
    'city': 'Kolkata',
    'state': 'WB',
    'street': '123 Main St',
    'zip_code': '700001'
}


# ============================================================
# STEP 4: CREATE AN ADDRESS OBJECT
# ============================================================

# Convert the dictionary into an Address model instance.
# The ** operator unpacks dictionary key-value pairs into keyword arguments.
# Pydantic validates the provided fields and creates the object.

address1 = Address(**address_dict)


# ============================================================
# STEP 5: CREATE PATIENT DATA
# ============================================================

# Create a dictionary containing the patient's personal information.
# The address field receives the Address object created above.
# Since gender is not provided, its default value will be used.

patient_data = {
    "name": "John Doe",
    "email": "john@gmail.com",
    "age": 67,
    "address": address1
}


# ============================================================
# STEP 6: CREATE THE PATIENT OBJECT
# ============================================================

# Unpack patient_data and pass its values to the Patient model.
# Pydantic validates the patient fields and the nested Address object.
# The result is a Patient model instance, not a Python dictionary.

patient1 = Patient(**patient_data)


# ============================================================
# STEP 7: DISPLAY PATIENT INFORMATION
# ============================================================

# Print the complete Patient object, including its nested address.
print("Patient Information:")
print(patient1)

# Access individual fields using dot notation.
print("\nPatient Name:", patient1.name)
print("Patient Email:", patient1.email)
print("Patient Age:", patient1.age)

# Access fields inside the nested Address object.
# patient1.address returns the Address model instance.
print("\nPatient Address:")
print("Street:", patient1.address.street)
print("City:", patient1.address.city)
print("State:", patient1.address.state)
print("ZIP Code:", patient1.address.zip_code)


# ============================================================
# STEP 8: model_dump()
# ============================================================

# model_dump() converts a Pydantic model instance into a Python dictionary.
# All fields are included by default.
# Nested Pydantic models are also converted into nested dictionaries.

temp = patient1.model_dump()


# ============================================================
# STEP 9: model_dump(include={...})
# ============================================================

# include selects only the specified fields for the output dictionary.
# Here, only name, email, and address are included.
# Fields such as age and gender are excluded from the result.

temp2 = patient1.model_dump(
    include={'name', 'email', 'address'}
)


# ============================================================
# STEP 10: model_dump(exclude={...})
# ============================================================

# exclude removes the specified fields from the output dictionary.
# Here, name, email, and address are excluded.
# The remaining fields, age and gender, are included.

temp3 = patient1.model_dump(
    exclude={'name', 'email', 'address'}
)


# ============================================================
# STEP 11: model_dump(exclude_unset=True)
# ============================================================

# exclude_unset=True excludes fields that were not explicitly provided
# when the Patient model instance was created.
# The gender field is omitted because its default value was used.
# Other explicitly provided fields, including address, are included.
# Note: gender still exists on patient1 and its value is "Male".

temp4 = patient1.model_dump(exclude_unset=True)


# ============================================================
# STEP 12: CHECK THE RETURN TYPES
# ============================================================

# model_dump() returns a Python dictionary in each of these examples.
# type() is used to check the data type of each returned object.

print(type(temp))
print(type(temp2))
print(type(temp3))
print(type(temp4))
