#python3 -m pip install "pydantic"
#python3 -m pip install "pydantic[email]"
from pydantic import BaseModel,EmailStr,AnyUrl
from typing import List, Dict ,Optional#Use for 2 level validation
# Step 1: Create a Pydantic model
#by defult every feild require in pydantic model thier we use Optional
class Patient(BaseModel):
    name: str
    #for email validation we have pydantic validation EmailStr
    email:EmailStr
    linkedin_url:AnyUrl
    age: int
    weight:float
    married:bool=False #defaul value set 
    #list have to import from Typing module
    allergies:Optional[List[str]]=None
    contact_details: Optional[Dict[str,str]]=None


# Step 2: Create patient data
patient_info = {
    "name": "Nitesh",
    "email":"abc@gmail.com",
    "linkedin_url":'http://linkedin.com/123',
    "age": 30,
    "weight":50.2,
    # "married":True,
    # "allergies":['pollen','dust'],
    # "contact_details":{'email':'abc@gmail.com','phone':'2345678899'}
}


# Step 3: Convert dictionary into a Patient object
patient1 = Patient(**patient_info)
# Step 4: Create a function that accepts a Patient object
def insert_patient_data(patient: Patient):
    print("Name: ", patient.name)
    print("Linedin Url: ",patient.linkedin_url)
    print("Email: ",patient.email)
    print("Age: ", patient.age)
    print("Marriend: ", patient.married)
    print("Patient data inserted successfully.")


def update_patient_data(patient:Patient):
    print("Name: ",patient.name)
    print("Age: ",patient.age)
    print("Weight: ",patient.weight)#if i give weight as string so automaticly pydantic can type cast to float as per model we created
    print("Allergies: ",patient.allergies)
    print("Contact Details: ",patient.contact_details)
    print("Patient data updated successfuly")

# Step 6: Pass the Patient object
insert_patient_data(patient1)

update_patient_data(patient1)



