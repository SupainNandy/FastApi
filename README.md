# FastAPI Learning — Python Backend Development

A hands-on journey into **FastAPI and REST API development using Python**. This repository contains practical examples, beginner-friendly code, and step-by-step exercises covering API fundamentals, JSON data handling, path parameters, query parameters, exception handling, and data sorting.

The goal is to build a strong foundation in backend development by implementing concepts through small, working examples.

## Tech Stack

- **Python** — Programming language
- **FastAPI** — Web framework for building REST APIs
- **Uvicorn** — ASGI server for running the application
- **JSON** — File-based data storage for learning API operations
- **Git & GitHub** — Version control and project management

## Project Structure

```text
fastApi/
├── 1_Lecture/
│   ├── main.py
│   └── patient.json
├── README.md
└── ...
```

The structure above illustrates the current learning module. Other lecture folders may contain additional examples as the repository grows.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/SupainNandy/fastApi.git
cd fastApi
```

### 2. Navigate to the Learning Directory

```bash
cd 1_Lecture
```

### 3. Create a Virtual Environment

**Ubuntu / Linux**

```bash
python3 -m venv myenv
source myenv/bin/activate
```

**Windows**

```bash
python -m venv myenv
myenv\Scripts\activate
```

### 4. Install Dependencies

```bash
python -m pip install fastapi uvicorn
```

### 5. Run the Application

If your Python application is saved as `main.py`:

```bash
uvicorn main:app --reload
```

The server will usually run at `http://127.0.0.1:8000`.

## Concepts Learned

### 1. Creating a FastAPI Application

FastAPI provides a simple way to create HTTP endpoints using Python functions and decorators.

```python
from fastapi import FastAPI

app = FastAPI(
    title="My First FastAPI",
    description="My first Python API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "FastAPI is running!"}
```

**What I learned:**
- Creating a FastAPI application instance.
- Using `@app.get()` to define GET endpoints.
- Returning Python dictionaries as JSON responses.
- Adding a title, description, and version to API documentation.

### 2. Creating Multiple GET Endpoints

Different endpoints can provide different information.

| Endpoint | Purpose |
|---|---|
| `/` | Check whether the API is running |
| `/about` | Return project information |
| `/patient` | Fetch all patient records |
| `/patient/{pid}` | Fetch a patient by ID |
| `/sort` | Sort patient records by a selected field |

Example:

```python
@app.get("/about")
def about():
    return {
        "project": "FastAPI",
        "status": "success"
    }
```

Each endpoint has a specific responsibility, which makes an API easier to organize and understand.

### 3. Reading JSON Data from a File

The project uses a `patient.json` file as its data source.

```python
import json
from pathlib import Path

def load_data():
    file_path = Path(__file__).resolve().parent / "patient.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
```

**How it works:**

- `__file__` identifies the current Python file.
- `Path(__file__).resolve().parent` identifies its containing directory.
- `/ "patient.json"` builds the path to the JSON file.
- `open()` opens the file in read mode.
- `json.load(file)` converts JSON content into Python objects, such as lists and dictionaries.

Using `Path` this way avoids depending on the terminal's current working directory.

The patient endpoint returns the loaded records:

```python
@app.get("/patient")
def fetch_data():
    return load_data()
```

This approach is useful for learning how an API reads and returns structured data before introducing a database.

### 4. Path Parameters

A path parameter is a value embedded in the URL path. It is commonly used to identify one particular resource.

**Example request:**

```http
GET /patient/3
```

**Implementation:**

```python
from fastapi import HTTPException, Path

@app.get("/patient/{pid}")
def fetch_patient_by_id(
    pid: int = Path(
        ...,
        description="Id of the patient in the database"
    )
):
    patients = load_data()

    for patient in patients:
        if patient["id"] == pid:
            return patient

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )
```

**What I learned:**

- `{pid}` defines a dynamic segment in the URL.
- `pid: int` declares the expected parameter type.
- `Path(...)` marks the parameter as required and adds documentation.
- The loop searches the loaded patient records for a matching ID.
- `HTTPException` returns an appropriate error if no patient matches.

If the patient exists, the endpoint returns that patient's record. Otherwise, it returns a `404 Not Found` response.

FastAPI also validates the integer type automatically. For example, `/patient/abc` produces a validation error because `abc` is not an integer.

### 5. Query Parameters

Query parameters are passed after `?` in a URL. They are useful for filtering, searching, sorting, and pagination.

In this project, query parameters control the sorting field and order.

**Example requests:**

```http
GET /sort?sort_by=height&order=asc
GET /sort?sort_by=weight&order=desc
GET /sort?sort_by=bmi&order=asc
```

**Implementation:**

```python
from fastapi import Query

@app.get("/sort")
def sort_patients(
    sort_by: str = Query(
        ...,
        description="Sort by height, weight, or bmi"
    ),
    order: str = Query(
        "asc",
        description="Sort in asc or desc order"
    )
):
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field; select from {valid_fields}"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order; select asc or desc"
        )

    data = load_data()

    sorted_flag = True if order == "desc" else False

    return sorted(
        data,
        key=lambda patient: patient[sort_by],
        reverse=sorted_flag
    )
```

**What I learned:**

- `Query(...)` makes `sort_by` required.
- `Query("asc")` sets ascending order as the default.
- A list of valid fields prevents sorting by unsupported fields.
- The API validates whether the requested order is `asc` or `desc`.
- Python's `sorted()` returns a new sorted list without changing the original list.
- `lambda` provides a compact function for selecting the sorting value.
- `reverse=True` sorts in descending order.

For example, `/sort?sort_by=height&order=desc` returns patient records ordered from greatest to smallest height.

### 6. Lambda Functions and Sorting

A lambda function is a small anonymous function that can be written in one expression.

```python
lambda patient: patient[sort_by]
```

Suppose a patient record looks like this:

```json
{
    "id": 1,
    "name": "Rahul",
    "height": 175,
    "weight": 70,
    "bmi": 22.9
}
```

When `sort_by` is `"height"`, the lambda behaves like:

```python
def get_sort_value(patient):
    return patient["height"]
```

Therefore:

```python
sorted(
    data,
    key=lambda patient: patient[sort_by],
    reverse=True
)
```

means: sort the patient records using the selected field, in descending order.

This technique can also be used when sorting products by price, employees by salary, or students by marks.

### 7. HTTP Exception Handling

`HTTPException` allows the API to return meaningful error responses.

```python
raise HTTPException(
    status_code=404,
    detail="Patient not found"
)
```

Common status codes:

| Status code | Meaning | Example |
|---|---|---|
| `200` | OK | Records returned successfully |
| `400` | Bad Request | Unsupported sorting field |
| `404` | Not Found | Patient ID does not exist |
| `422` | Unprocessable Entity | Invalid path parameter type |
| `500` | Internal Server Error | Unexpected server-side failure |

The project currently uses `400` for invalid sorting options and `404` when a patient cannot be found.

### 8. Interactive API Documentation

FastAPI automatically generates API documentation from the application and its parameter definitions.

After starting the server, open:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

Use Swagger UI to test the endpoints, provide path and query parameters, and inspect JSON responses and validation errors.

## Learning Roadmap

The repository will grow as I continue learning FastAPI and backend development.

- [x] Create a FastAPI application
- [x] Create basic GET endpoints
- [x] Read data from a JSON file
- [x] Implement path parameters
- [x] Fetch individual patient records by ID
- [x] Implement query parameters
- [x] Validate sorting fields and order
- [x] Sort JSON records using `sorted()` and `lambda`
- [ ] Implement POST endpoints to create records
- [ ] Learn request bodies and Pydantic models
- [ ] Implement PUT and PATCH endpoints
- [ ] Implement DELETE endpoints
- [ ] Learn routers and dependency injection
- [ ] Connect a database such as PostgreSQL
- [ ] Implement authentication and authorization
- [ ] Write API tests

## Useful Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python Documentation](https://docs.python.org/3/)
- [Python JSON Documentation](https://docs.python.org/3/library/json.html)
- [Python pathlib Documentation](https://docs.python.org/3/library/pathlib.html)

## Author

**Supain Nandy**

- GitHub: [@SupainNandy](https://github.com/SupainNandy)
- Repository: [FastAPI Learning](https://github.com/SupainNandy/fastApi)

---

*Learning Python backend development through practical implementation, one API at a time.*
