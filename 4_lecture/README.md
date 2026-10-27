# Patient Management API

A REST API built with **Python, FastAPI, and Pydantic** to manage patient records stored in a local JSON file. This project demonstrates request validation, path and query parameters, CRUD operations, sorting, and computed fields.

## Tech Stack

- **Python** — application logic
- **FastAPI** — API routes and interactive documentation
- **Pydantic** — request validation and computed fields
- **JSON** — file-based data storage
- **Uvicorn** — ASGI server

## Features

- View API status and project information.
- Retrieve all patients or fetch one patient by ID.
- Validate patient data using Pydantic.
- Validate email addresses with `EmailStr`.
- Apply constraints to age, height, and weight.
- Calculate BMI and a BMI verdict automatically.
- Sort patients by height, weight, or BMI.
- Create patients while preventing duplicate IDs.
- Update existing patient records with `PUT`.
- Delete patient records with `DELETE`.
- Return HTTP errors when a patient is not found or data is invalid.

## Project Structure

```text
project/
├── main.py       # FastAPI application and endpoints
├── patient.json  # Patient records stored as a JSON array
└── README.md     # Project documentation
```

The code resolves `patient.json` from the parent directory of the directory containing `main.py`. Adjust `get_data_file_path()` if your file is stored elsewhere.

## Setup and Run

### 1. Create and activate a virtual environment

**Windows PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```bat
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install fastapi uvicorn "pydantic[email]"
```

The `pydantic[email]` extra installs the dependency required for `EmailStr` validation.

### 3. Prepare `patient.json`

Create a JSON file containing a list of patient records. For example:

```json
[
  {
    "id": 1,
    "name": "Aarav Sharma",
    "city": "Kolkata",
    "email": "aarav@example.com",
    "age": 28,
    "height": 175,
    "weight": 70,
    "gender": "Male"
  }
]
```

The `bmi` and `verdict` fields can be omitted because the `Patient` model calculates them. Ensure the file exists and contains valid JSON before starting the API.

### 4. Start the server

If the Python file is named `main.py`:

```bash
uvicorn main:app --reload
```

- API root: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/` | Return an API status message |
| `GET` | `/about` | Return project information |
| `GET` | `/patient` | Retrieve all patient records |
| `GET` | `/patient/{pid}` | Retrieve a patient by ID |
| `GET` | `/sort?sort_by=weight&order=desc` | Sort by height, weight, or BMI |
| `POST` | `/create` | Create a patient |
| `PUT` | `/edit/{pid}` | Update editable patient details |
| `DELETE` | `/delete/{pid}` | Delete a patient |

## Today's Learning: PUT and DELETE

### 1. PUT — Update a patient

The `PUT /edit/{pid}` endpoint updates the editable details of an existing patient.

**Example request:**

```http
PUT http://127.0.0.1:8000/edit/1
Content-Type: application/json
```

```json
{
  "name": "Aarav Sharma",
  "city": "Kolkata",
  "email": "aarav.updated@example.com",
  "age": 29,
  "height": 175,
  "weight": 72,
  "gender": "Male"
}
```

**How it works:**

1. Receives the patient ID from the URL path.
2. Loads records from `patient.json`.
3. Searches for the patient whose `id` matches `pid`.
4. Converts the validated `PatientUpdate` model into a dictionary using `model_dump()`.
5. Updates the editable fields while keeping the original patient ID unchanged.
6. Validates the updated record again using the `Patient` model.
7. Recalculates the computed `bmi` and `verdict` fields.
8. Saves the updated records to `patient.json`.
9. Returns a success message and the updated patient.

**Possible responses:**

- `200 OK` — patient updated successfully.
- `404 Not Found` — no patient exists with that ID.
- `422 Unprocessable Entity` — request data fails FastAPI/Pydantic validation.

**Important:** `PatientUpdate` requires all editable fields, so this endpoint performs a full update of those fields, not a partial update. A `PATCH` endpoint is typically used when only selected fields should change.

### 2. DELETE — Remove a patient

The `DELETE /delete/{pid}` endpoint removes a patient record by ID.

**Example request:**

```http
DELETE http://127.0.0.1:8000/delete/1
```

**How it works:**

1. Receives the patient ID from the URL path.
2. Loads the patient list from `patient.json`.
3. Searches for the matching patient.
4. Removes the record using `pop(index)`.
5. Saves the remaining records to the JSON file.
6. Returns a success message and the deleted record.

**Possible responses:**

- `200 OK` — patient deleted successfully.
- `404 Not Found` — no patient exists with that ID.
- `422 Unprocessable Entity` — the path parameter is not a valid integer.

## Other Concepts in This Project

### Pydantic models

- `Patient` validates a complete patient record, including its ID.
- `PatientUpdate` validates editable fields and does not accept an ID in the request body.
- `EmailStr` validates email address format.
- `Field` defines constraints and descriptions for API documentation.
- `Literal["Male", "Female", "Other"]` restricts gender to the listed values.
- `Annotated` combines type hints with FastAPI and Pydantic metadata.

### Computed fields

The `bmi` property converts height from centimetres to metres and calculates:

```text
BMI = weight in kilograms / (height in metres × height in metres)
```

The `verdict` property uses these thresholds:

| BMI | Verdict |
| --- | --- |
| Below 18.5 | Underweight |
| 18.5 to below 25 | Normal weight |
| 25 to below 30 | Overweight |
| 30 or above | Obese |

These are simplified adult BMI categories, not a medical diagnosis.

### Path and query parameters

- **Path parameter:** `/patient/1` identifies a patient by ID.
- **Query parameters:** `/sort?sort_by=height&order=asc` specifies sorting criteria.
- Supported sort fields are `height`, `weight`, and `bmi`; supported orders are `asc` and `desc`.

### JSON file storage

The `load_data()` and `save_data()` helper functions read and write patient records in `patient.json`. JSON is convenient for learning, but a production API would generally use a database and safer concurrent-write handling.

## Test PUT and DELETE in Swagger UI

1. Start the server.
2. Open `http://127.0.0.1:8000/docs`.
3. Expand `PUT /edit/{pid}`, enter an existing patient ID, provide all required fields, and execute the request.
4. Expand `DELETE /delete/{pid}`, enter a patient ID, and execute the request.
5. Use `GET /patient` to inspect the remaining records.

Be careful when testing `DELETE`: it permanently removes the record from the local JSON file unless you restore it from a backup.

## Learning Summary

Today I practised:

- Building REST API endpoints with FastAPI.
- Validating request bodies with Pydantic.
- Using `PUT` to update an existing record.
- Using `DELETE` to remove a record.
- Handling missing records with `HTTPException`.
- Returning JSON responses and HTTP status codes.
- Revalidating updated records and recalculating computed fields.
- Saving changes to a JSON file.

## Future Improvements

- Add `PATCH` for partial updates.
- Move from JSON storage to PostgreSQL or another database.
- Add automated tests with `pytest` and FastAPI's `TestClient`.
- Add authentication and authorization.
- Add structured logging and safer file-write handling.
