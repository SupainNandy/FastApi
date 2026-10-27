# FastAPI Patient Management API

A beginner-friendly REST API built with **FastAPI** and **Pydantic**.
This project demonstrates how to create a POST endpoint, validate
incoming request data, calculate derived fields, handle errors, and
store patient records in a JSON file.

## Learning Goals

In this lesson, I learned how to:

-   Create a FastAPI application and define API endpoints.
-   Use HTTP `GET` and `POST` methods.
-   Accept request-body data through a Pydantic model.
-   Validate data types and enforce field constraints.
-   Validate email addresses using `EmailStr`.
-   Restrict a field to specific values using `Literal`.
-   Use `Annotated` with Pydantic's `Field`, FastAPI's `Path`, and
    `Query`.
-   Calculate BMI and a BMI category with Pydantic computed fields.
-   Read from and write to a JSON file.
-   Return suitable HTTP status codes and error responses.
-   Explore and test endpoints through Swagger UI.

## Technology Stack

-   **Python** --- application language
-   **FastAPI** --- web framework for building APIs
-   **Pydantic v2** --- request-data validation and serialization
-   **Uvicorn** --- ASGI server
-   **JSON** --- simple file-based data storage

## Project Structure

``` text
1_Lecture/
├── myenv/          # Python virtual environment (local)
├── main.py         # FastAPI application and endpoints
├── patient.json    # Patient records stored as a JSON array
└── README.md       # Project documentation
```

Example `patient.json` starting content:

``` json
[]
```

If you already have patient records, keep the file as a valid JSON array
of objects. Each record used by the sorting endpoint should include
`id`, `name`, `age`, `height`, `weight`, `gender`, and `email` as
applicable. The BMI sort calculates BMI from `height` and `weight`.

## Installation and Setup

Commands below are for Windows Git Bash when `myenv` is inside
`1_Lecture/`.

### 1. Open the project directory

``` bash
cd ~/Desktop/got/fastApi/1_Lecture
```

### 2. Create a virtual environment (if needed)

``` bash
python -m venv myenv
```

### 3. Activate the virtual environment

``` bash
source myenv/Scripts/activate
```

If activation fails, check the folder with `ls myenv`. A Windows virtual
environment normally contains `Scripts/`; a Linux/macOS environment
normally contains `bin/`.

### 4. Install dependencies

``` bash
python -m pip install fastapi "uvicorn[standard]" "pydantic[email]"
```

`pydantic[email]` installs the optional email-validation dependency
required by `EmailStr`.

### 5. Start the development server

``` bash
python -m uvicorn main:app --reload
```

The command assumes the Python file is named `main.py` and the FastAPI
instance is named `app`.

-   API base URL: `http://127.0.0.1:8000`
-   Swagger UI: `http://127.0.0.1:8000/docs`
-   ReDoc: `http://127.0.0.1:8000/redoc`

Stop the server with `Ctrl + C`.

## Pydantic Model and Field Validation

The `Patient` class inherits from `BaseModel`. FastAPI uses this model
to parse and validate the JSON body sent to the `POST /create` endpoint.
If the incoming body does not meet the model requirements, FastAPI
returns a `422 Unprocessable Entity` response before the endpoint
function runs.

### Field-by-field rules

  --------------------------------------------------------------------------------------
  Field                   Type or rule                           Purpose
  ----------------------- -------------------------------------- -----------------------
  `id`                    `int`                                  Unique patient
                                                                 identifier; duplicate
                                                                 IDs are checked in the
                                                                 endpoint

  `name`                  `str`                                  Patient's name

  `email`                 `EmailStr`                             Must be a valid email
                                                                 address

  `age`                   `int`, `gt=0`, `lt=120`                Must be greater than 0
                                                                 and less than 120

  `height`                `float`, `gt=0`                        Height in centimeters;
                                                                 must be positive

  `weight`                `float`, `gt=0`                        Weight in kilograms;
                                                                 must be positive

  `gender`                `Literal["Male", "Female", "Other"]`   Accepts only one of the
                                                                 listed values

  `bmi`                   `@computed_field`                      Calculated from height
                                                                 and weight

  `verdict`               `@computed_field`                      Derived BMI category
  --------------------------------------------------------------------------------------

### What does `Annotated` do?

`Annotated` attaches metadata to a type without replacing the underlying
type.

``` python
age: Annotated[int, Field(gt=0, lt=120)]
```

This means that `age` is an integer and Pydantic must enforce the
constraints:

-   `gt=0`: greater than zero
-   `lt=120`: less than 120

`Field(...)` can also provide descriptions, defaults, and other schema
or validation metadata. In this model, `...` means the field is
required.

### Important distinction: validation vs. a custom field validator

This project currently uses built-in Pydantic field constraints
(`Field`), a specialized email type (`EmailStr`), and `Literal`. These
are forms of validation, but the code does **not** currently define a
custom `@field_validator` method.

A custom field validator is useful when you need your own validation
logic, such as trimming whitespace or checking a business-specific rule:

``` python
from pydantic import BaseModel, field_validator

class Example(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be blank")
        return value
```

Pydantic runs this validator while validating the `name` field. Raising
`ValueError` causes validation to fail, and FastAPI normally reports the
request-body validation error as HTTP 422.

### Common validation outcomes

-   Missing a required field: validation error.
-   Sending an invalid email: validation error.
-   Sending an age of `0` or `120`: validation error.
-   Sending a negative height or weight: validation error.
-   Sending a gender other than `Male`, `Female`, or `Other`: validation
    error.
-   Sending a duplicate patient ID: the endpoint returns HTTP
    `400 Bad Request`.

## Computed Fields: BMI and Verdict

Pydantic's `@computed_field` includes a property in the model's
serialized output. It is not a value the client needs to provide in the
POST request.

### BMI formula

BMI is calculated as:

``` text
BMI = weight in kilograms / (height in meters)²
```

The model stores height in centimeters, so the code converts it to
meters first:

``` python
height_in_meters = self.height / 100
return round(self.weight / (height_in_meters ** 2), 2)
```

The `verdict` property classifies the calculated BMI using common adult
BMI ranges:

-   Below 18.5: Underweight
-   18.5 to below 25: Normal weight
-   25 to below 30: Overweight
-   30 or above: Obese

These are general adult BMI categories, not a medical diagnosis. BMI
interpretation differs for children and some other populations.

## API Endpoints

  ----------------------------------------------------------------------------------
  Method                  Endpoint                           Purpose
  ----------------------- ---------------------------------- -----------------------
  `GET`                   `/`                                Check that the API is
                                                             running

  `GET`                   `/about`                           Return basic project
                                                             information

  `GET`                   `/patient`                         Return all patient
                                                             records

  `GET`                   `/patient/{pid}`                   Find a patient by ID

  `GET`                   `/sort?sort_by=height&order=asc`   Sort patients by
                                                             height, weight, or BMI

  `POST`                  `/create`                          Validate and create a
                                                             patient record
  ----------------------------------------------------------------------------------

### 1. Home

``` http
GET /
```

Example response:

``` json
{
  "message": "FastAPI is running!"
}
```

### 2. About

``` http
GET /about
```

### 3. Fetch all patients

``` http
GET /patient
```

Returns the contents of `patient.json`.

### 4. Fetch one patient by ID

``` http
GET /patient/1
```

The `pid` path parameter is converted to an integer and validated. If no
matching patient exists, the endpoint raises HTTP `404 Not Found`.

### 5. Sort patients

Examples:

``` http
GET /sort?sort_by=height&order=asc
GET /sort?sort_by=weight&order=desc
GET /sort?sort_by=bmi&order=asc
```

-   `sort_by` is required and accepts `height`, `weight`, or `bmi`.
-   `order` is optional and defaults to `asc`; supported values are
    `asc` and `desc`.
-   Invalid values produce HTTP `400 Bad Request`.
-   BMI is calculated from height and weight for sorting.

### 6. Create a patient (POST)

``` http
POST /create
Content-Type: application/json
```

Example request body:

``` json
{
  "id": 6,
  "name": "Aarav Sharma",
  "email": "aarav.sharma@example.com",
  "age": 28,
  "height": 175,
  "weight": 70,
  "gender": "Male"
}
```

Do not include `bmi` or `verdict` in the request body; the model
calculates them.

Example successful response (HTTP `201 Created`):

``` json
{
  "message": "Patient created successfully",
  "patient": {
    "id": 6,
    "name": "Aarav Sharma",
    "email": "aarav.sharma@example.com",
    "age": 28,
    "height": 175.0,
    "weight": 70.0,
    "gender": "Male",
    "bmi": 22.86,
    "verdict": "Normal weight"
  }
}
```

The endpoint checks for a duplicate ID, appends the serialized patient
to the list, and writes the updated list to `patient.json`.

## How to Test the POST Endpoint

1.  Start the server.
2.  Open `http://127.0.0.1:8000/docs`.
3.  Expand **POST `/create`**.
4.  Select **Try it out**.
5.  Paste the example JSON request body.
6.  Select **Execute**.
7.  Inspect the HTTP status and response body.
8.  Open **GET `/patient`** to verify that the record was saved.

Try changing the request to test validation:

-   Set `"age": 0`.
-   Set `"email": "not-an-email"`.
-   Set `"height": -175`.
-   Set `"gender": "Unknown"`.
-   Submit the same ID twice.

Expected outcomes include HTTP `422` for model validation failures and
HTTP `400` for a duplicate ID.

## Important Concepts Learned

### Request body

The parameter `patient: Patient` tells FastAPI to read the incoming JSON
body and validate it against the `Patient` model.

### Path parameter

`/patient/{pid}` captures a value from the URL path.

### Query parameters

`/sort?sort_by=height&order=asc` sends optional or required values in
the URL query string.

### HTTP status codes

-   `200 OK`: successful GET request by default.
-   `201 Created`: patient successfully created.
-   `400 Bad Request`: duplicate ID or invalid sorting options in this
    project.
-   `404 Not Found`: requested patient does not exist.
-   `422 Unprocessable Entity`: request data failed validation.

### JSON persistence

The project uses `json.load()` to read records and `json.dump()` to
write records. This is suitable for a learning exercise, but it is not a
replacement for a database in a production application.

## Notes and Limitations

-   Ensure `patient.json` exists and contains valid JSON before making
    requests.
-   File writes are not designed for concurrent requests; simultaneous
    updates can overwrite one another.
-   The duplicate-ID check is application-level and is not safe against
    concurrent writes.
-   `@computed_field` is part of Pydantic v2.
-   The code uses `model_dump()`, the recommended Pydantic v2
    serialization method.
-   The current `Patient` model validates new POST requests, but
    existing JSON records returned by GET endpoints are not
    automatically revalidated against that model.
-   For a production project, consider a database, database-level unique
    constraints, tests, and stronger error handling for file access or
    invalid JSON.

## Summary

This lesson covers the basic workflow of a FastAPI POST request:

1.  Receive a JSON request body.
2.  Validate its fields with Pydantic.
3.  Reject invalid input automatically.
4.  Calculate derived fields with computed properties.
5.  Check for duplicate IDs.
6.  Serialize the model using `model_dump()`.
7.  Save the new record to JSON.
8.  Return an HTTP response with the appropriate status code.

The next useful step is to practice custom `@field_validator` methods
and `@model_validator` for validation rules that involve one or more
fields.
