# FastAPI Fundamentals — Lecture 1

A beginner-friendly introduction to FastAPI, covering environment setup, creating REST API endpoints, reading JSON data, handling path and query parameters, and sorting records.

## Topics Covered

- FastAPI installation and project setup
- Creating a FastAPI application
- Defining GET endpoints
- Reading data from a JSON file
- Path parameters using `Path()`
- Query parameters using `Query()`
- Handling errors with `HTTPException`
- Sorting patient records dynamically

## 1. Project Setup

### Create a virtual environment

```bash
python3 -m venv myenv
```

### Activate the virtual environment

**Ubuntu / Linux**

```bash
source myenv/bin/activate
```

**Windows**

```bash
myenv\Scripts\activate
```

### Install dependencies

```bash
pip install fastapi uvicorn
```

## 2. Project Structure

```text
1_Lecture/
├── main.py
├── patient.json
├── README.md
└── myenv/
```

- `main.py` — Contains the FastAPI application and API endpoints.
- `patient.json` — Stores patient records in JSON format.
- `README.md` — Documents the concepts covered in this lecture.
- `myenv/` — Contains the project's virtual environment.

## 3. Run the Application

Start the development server using:

```bash
uvicorn main:app --reload
```

Open the following URLs in your browser:

| URL | Purpose |
|---|---|
| `http://127.0.0.1:8000/` | Home endpoint |
| `http://127.0.0.1:8000/about` | About endpoint |
| `http://127.0.0.1:8000/patient` | Fetch all patients |
| `http://127.0.0.1:8000/docs` | Interactive API documentation |

## 4. Creating Basic API Endpoints

### Home endpoint

```python
@app.get("/")
def home():
    return {"message": "FastAPI is running!"}
```

This endpoint returns a JSON response when a user visits the root URL.

### About endpoint

```python
@app.get("/about")
def about():
    return {
        "project": "FastAPI",
        "status": "success"
    }
```

This endpoint returns basic information about the project.

## 5. Reading Data from a JSON File

The `load_data()` function reads patient records from `patient.json`.

```python
def load_data():
    file_path = FilePath(__file__).resolve().parent / "patient.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
```

### How it works

1. `__file__` identifies the current Python file.
2. `resolve().parent` locates the directory containing `main.py`.
3. `open()` opens the JSON file in read mode.
4. `json.load()` converts the JSON contents into Python objects.

The API endpoint returns the patient records:

```python
@app.get("/patient")
def fetch_data():
    return load_data()
```

## 6. Path Parameters and `Path()`

Path parameters allow us to retrieve a specific resource using a value included in the URL.

### Example

```python
@app.get("/patient/{pid}")
def fetch_patient_by_id(
    pid: int = Path(
        ...,
        description="ID of the patient in the database"
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

### How it works

- `{pid}` represents a dynamic value in the URL.
- `pid: int` declares that the parameter should be an integer.
- `Path(...)` makes the parameter required and adds documentation.
- The loop searches for a patient whose ID matches `pid`.
- `HTTPException` returns a 404 error if the patient does not exist.

### Test the endpoint

```text
GET /patient/1
GET /patient/2
GET /patient/100
```

The first two requests return matching records if those IDs exist. The last request returns a 404 response if patient 100 is not found.

## 7. Query Parameters and `Query()`

Query parameters pass additional information through the URL after a question mark (`?`).

They are useful for filtering, sorting, searching, and pagination.

### Example

```python
@app.get("/sort")
def sort_patients(
    sort_by: str = Query(
        ...,
        description="Sort by height, weight, or bmi"
    ),
    order: str = Query(
        "asc",
        description="Sort in asc or desc order"
    ),
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

### Test the endpoint

Sort patients by height in ascending order:

```text
http://127.0.0.1:8000/sort?sort_by=height&order=asc
```

Sort patients by weight in descending order:

```text
http://127.0.0.1:8000/sort?sort_by=weight&order=desc
```

Sort patients by BMI:

```text
http://127.0.0.1:8000/sort?sort_by=bmi
```

If `order` is omitted, the API uses `asc` by default.

### Understanding `Query()`

- `sort_by: str` accepts the field to sort by.
- `Query(...)` makes `sort_by` a required parameter.
- `order: str = Query("asc")` provides a default value.
- `valid_fields` prevents sorting by unsupported fields.
- `sorted()` creates a sorted list without modifying the original list.
- `reverse=True` sorts in descending order.

## 8. Understanding `Path()` vs `Query()`

| Feature | `Path()` | `Query()` |
|---|---|---|
| Purpose | Identifies a resource | Controls filtering or sorting |
| Location | Inside the URL path | After `?` in the URL |
| Example | `/patient/1` | `/sort?sort_by=height` |
| Typical use | Fetch one patient by ID | Sort patient records |
| Default values | Path parameters are required | Query parameters can have defaults |

**Simple rule:** Use path parameters to identify a resource and query parameters to customize the results.

## 9. Handling HTTP Errors

FastAPI provides `HTTPException` to return meaningful HTTP error responses.

```python
raise HTTPException(
    status_code=404,
    detail="Patient not found"
)
```

Common status codes:

- `200 OK` — The request succeeded.
- `400 Bad Request` — The request contains invalid input.
- `404 Not Found` — The requested resource does not exist.
- `422 Unprocessable Entity` — Request parameter validation failed.

## 10. Interactive API Documentation

FastAPI automatically generates interactive API documentation.

**Swagger UI:** `http://127.0.0.1:8000/docs`

**ReDoc:** `http://127.0.0.1:8000/redoc`

You can inspect endpoints, enter parameters, execute requests, and view responses directly from your browser.

## 11. What I Learned

By completing this lecture, I learned how to:

- Set up a FastAPI development environment.
- Create and run a basic API server.
- Define GET endpoints.
- Read structured data from a JSON file.
- Retrieve individual records using path parameters.
- Document parameters with `Path()` and `Query()`.
- Validate input and handle errors.
- Sort JSON records dynamically using Python's `sorted()` function and a lambda expression.

## Next Steps

- Learn request bodies using Pydantic models.
- Implement POST, PUT, and DELETE endpoints.
- Add filtering and pagination.
- Connect FastAPI to a database.
- Build a complete CRUD application.

---

**Lecture:** 1 — FastAPI Fundamentals  
**Level:** Beginner  
**Framework:** FastAPI  
**Language:** Python
