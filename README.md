Beginner-friendly notes for learning FastAPI, building simple REST APIs, reading JSON files, and testing endpoints.

> **Note:** These notes cover foundational FastAPI concepts and a patient JSON API example. They are not a verified word-for-word transcript of the two linked videos. Add video transcripts/captions if you need exact, timestamped notes from each lecture.

## Table of Contents

1. [What is FastAPI?](#1-what-is-fastapi)
2. [What is an API?](#2-what-is-an-api)
3. [What is a REST API?](#3-what-is-a-rest-api)
4. [Install and Set Up FastAPI on Ubuntu](#4-install-and-set-up-fastapi-on-ubuntu)
5. [Create Your First API](#5-create-your-first-api)
6. [Understand the Code](#6-understand-the-code)
7. [Create Multiple Endpoints](#7-create-multiple-endpoints)
8. [Return HTML](#8-return-html)
9. [JSON and Python Dictionaries](#9-json-and-python-dictionaries)
10. [Read Data from a JSON File](#10-read-data-from-a-json-file)
11. [Automatic API Documentation](#11-automatic-api-documentation)
12. [Important Concepts](#12-important-concepts-to-revise)
13. [Common Errors and Fixes](#13-common-errors-and-fixes)
14. [Interview Questions and Answers](#14-interview-questions-and-answers)
15. [Practice Exercises](#15-practice-exercises)
16. [Video Links](#16-video-links)

## 1. What is FastAPI?

FastAPI is a modern Python web framework used to build APIs. It supports Python type hints, request validation, asynchronous programming, and automatically generated API documentation.

For example, a React frontend can request patient information from a FastAPI backend.

A typical application flow looks like this:

```text
React / Browser
      |
      | HTTP request
      v
FastAPI Backend
(routes, validation, business logic)
      |
      | database query
      v
PostgreSQL / MySQL / SQLite
```

### Why use FastAPI?

- Easy to learn if you already know Python.
- Uses Python type hints for request handling and validation.
- Generates interactive API documentation automatically.
- Supports `async` and `await`.
- Suitable for REST APIs, backend services, and AI/ML applications.

## 2. What is an API?

API stands for **Application Programming Interface**. It allows software applications to communicate with one another.

For example, a frontend can request patient details from a backend:

```http
GET /patients/1
```

The backend may return this JSON response:

```json
{
  "id": 1,
  "name": "Rahul",
  "city": "Kolkata"
}
```

Key terms:

- **Request:** What the client asks the server to do.
- **Response:** What the server sends back.
- **Endpoint:** A URL path used to access an API operation.
- **JSON:** A common data format for exchanging information.

## 3. What is a REST API?

REST is an architectural style commonly used to design web APIs.

| HTTP method | Purpose | Example |
|---|---|---|
| `GET` | Retrieve data | Get all patients |
| `POST` | Create data | Add a patient |
| `PUT` | Replace/update a resource | Replace a patient's details |
| `PATCH` | Partially update data | Update a patient's city |
| `DELETE` | Delete data | Remove a patient |

These methods are commonly used for CRUD operations:

- **C** — Create
- **R** — Read
- **U** — Update
- **D** — Delete

## 4. Install and Set Up FastAPI on Ubuntu

### Step 1: Create a project directory

```bash
mkdir fastapi-learning
cd fastapi-learning
```

### Step 2: Create a virtual environment

```bash
python3 -m venv myenv
```

Activate it:

```bash
source myenv/bin/activate
```

A virtual environment keeps dependencies isolated for this project.

If virtual-environment support is missing on Ubuntu, install it with:

```bash
sudo apt update
sudo apt install python3-venv
```

### Step 3: Install FastAPI

```bash
python -m pip install --upgrade pip
pip install "fastapi[standard]"
```

### Step 4: Start the development server

After creating `main.py` as shown below, run:

```bash
fastapi dev main.py
```

The development server usually runs at `http://127.0.0.1:8000`.

Useful URLs:

- API root: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

These URLs work while your local server is running.

## 5. Create Your First API

Create a file named `main.py`:

```python
from fastapi import FastAPI

app = FastAPI(
    title="My First FastAPI",
    description="My first Python API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Hello, World!"}
```

Run the app:

```bash
fastapi dev main.py
```

Open `http://127.0.0.1:8000/`. You should see:

```json
{
  "message": "Hello, World!"
}
```

## 6. Understand the Code

### Import FastAPI

```python
from fastapi import FastAPI
```

This imports the `FastAPI` class from the framework.

### Create the application

```python
app = FastAPI()
```

This creates the application instance. The server uses `app` to access your routes.

### Register a route

```python
@app.get("/")
```

This decorator registers the function below it to handle `GET` requests sent to the root path `/`.

### Return a response

```python
def home():
    return {"message": "Hello, World!"}
```

The function returns a Python dictionary. FastAPI serializes supported return values into a JSON response.

## 7. Create Multiple Endpoints

You can define multiple endpoints in one FastAPI application:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI"}

@app.get("/about")
def about():
    return {"message": "This is my first API"}

@app.get("/students")
def get_students():
    return [
        {"id": 1, "name": "Rahul"},
        {"id": 2, "name": "Priya"},
        {"id": 3, "name": "Amit"}
    ]
```

| Endpoint | Response |
|---|---|
| `/` | Welcome message |
| `/about` | About message |
| `/students` | List of students |

Try the endpoints in your browser or through Swagger UI at `/docs`.

**Remember:** FastAPI can automatically convert supported Python dictionaries and lists into JSON. You generally do not need to call `json.dumps()` yourself when returning them from an endpoint.

## 8. Return HTML

FastAPI can return HTML as well as JSON. Use `HTMLResponse` when you want the response to be interpreted as HTML.

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>My Website</title>
        </head>
        <body>
            <h1>Welcome to FastAPI</h1>
            <p>This is an HTML response.</p>
        </body>
    </html>
    """
```

The browser renders the HTML rather than showing a JSON object.

For larger applications, a template engine such as Jinja2 is usually easier to maintain than embedding long HTML strings in Python code.

## 9. JSON and Python Dictionaries

JSON stands for **JavaScript Object Notation**. It is a text format used to exchange structured data.

Python dictionary:

```python
patient = {
    "id": 1,
    "name": "Rahul",
    "city": "Kolkata",
    "age": 24
}
```

Equivalent JSON:

```json
{
  "id": 1,
  "name": "Rahul",
  "city": "Kolkata",
  "age": 24
}
```

Important differences:

- Python dictionaries can contain Python values such as `None`, `True`, and `False`.
- JSON uses `null`, `true`, and `false`.
- JSON object keys and string values use double quotes.
- Python's `json` module can read and write JSON data.

FastAPI handles conversion of supported Python return values to JSON responses automatically.

## 10. Read Data from a JSON File

This example creates a small patient API backed by a local JSON file.

### Project structure

```text
fastapi-learning/
├── main.py
├── patient.json
└── myenv/
```

### Create `patient.json`

```json
[
  {
    "id": 1,
    "name": "Rahul",
    "city": "Kolkata",
    "age": 24
  },
  {
    "id": 2,
    "name": "Priya",
    "city": "Delhi",
    "age": 22
  },
  {
    "id": 3,
    "name": "Amit",
    "city": "Mumbai",
    "age": 26
  }
]
```

### Create `main.py`

```python
from fastapi import FastAPI, HTTPException
import json
from pathlib import Path

app = FastAPI(
    title="Patient API",
    description="A beginner API that reads patients from a JSON file",
    version="1.0.0"
)

def load_data():
    file_path = Path(__file__).resolve().parent / "patient.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

@app.get("/")
def home():
    return {"message": "Patient API is running"}

@app.get("/patients")
def get_patients():
    return load_data()

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    patients = load_data()

    for patient in patients:
        if patient["id"] == patient_id:
            return patient

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )
```

### How does the JSON file get read?

1. `Path(__file__).resolve().parent` finds the directory containing `main.py`.
2. `/ "patient.json"` builds a path to the JSON file in that directory.
3. `open(file_path, "r", encoding="utf-8")` opens the file for reading.
4. `json.load(file)` parses the JSON into Python lists and dictionaries.
5. FastAPI converts the returned data into a JSON HTTP response.

### Test the endpoints

| Method | Endpoint | Expected result |
|---|---|---|
| `GET` | `/` | API status message |
| `GET` | `/patients` | All patients |
| `GET` | `/patients/1` | Rahul's record |
| `GET` | `/patients/99` | `404 Not Found` if ID 99 does not exist |

### What is a path parameter?

In this route:

```python
@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    ...
```

`{patient_id}` is a **path parameter**. FastAPI extracts its value from the URL and converts it to an integer because the function declares `patient_id: int`.

For example, `/patients/2` passes the value `2` to the function.

The `int` type annotation also allows FastAPI to validate the value. If a non-integer is supplied, FastAPI returns a validation error.

### Why use `HTTPException`?

```python
raise HTTPException(
    status_code=404,
    detail="Patient not found"
)
```

This returns an HTTP error response when the requested patient does not exist.

Example response:

```json
{
  "detail": "Patient not found"
}
```

A JSON file is useful for learning. For production applications, especially where records change frequently or several users may update data, use a database such as PostgreSQL or MySQL.

## 11. Automatic API Documentation

FastAPI generates interactive documentation from your application's routes and type annotations.

### Swagger UI — `/docs`

Open `http://127.0.0.1:8000/docs`.

Swagger UI allows you to:

- View available endpoints.
- Inspect HTTP methods and parameters.
- Execute requests from the browser.
- View response bodies and status codes.

### ReDoc — `/redoc`

Open `http://127.0.0.1:8000/redoc`.

ReDoc provides a structured API reference layout.

You do not need to manually create these documentation pages. FastAPI generates them from your application.

## 12. Important Concepts to Revise

| Concept | Meaning |
|---|---|
| Framework | Tools and conventions for building applications |
| API | Interface that allows applications to communicate |
| Endpoint | A path and method used to access an API operation |
| Route decorator | Connects a Python function to an HTTP method and path |
| JSON | Data exchange format |
| HTTP method | Describes the requested operation |
| Uvicorn | ASGI server commonly used to run FastAPI |
| Swagger UI | Interactive API documentation |
| ReDoc | API reference documentation |
| Virtual environment | Isolated Python dependency environment |
| Path parameter | Value extracted from the URL path |
| `HTTPException` | Mechanism for returning an HTTP error response |

## 13. Common Errors and Fixes

| Error | Possible fix |
|---|---|
| `python: command not found` | On Ubuntu, use `python3` to create the environment. |
| `ModuleNotFoundError: No module named 'fastapi'` | Activate the correct virtual environment and install FastAPI in it. |
| `Address already in use` | Stop the other server process or choose another port. |
| `404 Not Found` | Check the URL path and HTTP method. |
| JSON file not found | Check the filename and use `Path(__file__).resolve().parent` to locate the file relative to `main.py`. |
| Changes do not appear | Confirm the development server is running and refresh the endpoint. |
| Invalid JSON error | Validate the contents of `patient.json`; JSON does not allow trailing commas or Python-only values such as `None`. |

## 14. Interview Questions and Answers

### Q1. What is FastAPI?

FastAPI is a Python web framework for building APIs. It uses type hints, supports validation, and generates interactive API documentation.

### Q2. What is the difference between FastAPI and Flask?

Both are Python web frameworks. FastAPI emphasizes type-driven validation, generated documentation, and ASGI-based asynchronous support. Flask is a lightweight WSGI framework with a simple core and a flexible extension ecosystem.

### Q3. What is the purpose of `@app.get("/")`?

It registers a function to handle `GET` requests sent to the root path `/`.

### Q4. What is the difference between JSON and a Python dictionary?

A dictionary is a Python data structure. JSON is a text-based data format. FastAPI can serialize supported Python dictionaries into JSON responses.

### Q5. What is Uvicorn?

Uvicorn is an ASGI server that runs applications such as FastAPI and handles incoming HTTP connections.

### Q6. What is the purpose of `/docs`?

It provides interactive Swagger UI documentation generated from the FastAPI application.

### Q7. Why use `HTTPException`?

It allows an endpoint to return an HTTP error status and a detail message, such as `404 Not Found` when a patient does not exist.

### Q8. Can FastAPI return HTML?

Yes. It can return HTML using `HTMLResponse`, or use template engines such as Jinja2 for maintainable HTML pages.

### Q9. What is a path parameter?

A path parameter is a value captured from a URL path, such as `patient_id` in `/patients/{patient_id}`.

### Q10. What does `json.load(file)` do?

It reads JSON content from an open file and converts it into corresponding Python objects, such as dictionaries and lists.

## 15. Practice Exercises

Try completing these exercises without copying the solutions first.

1. **Create a health endpoint:** Add `GET /health` and return `{"status": "ok"}`.
2. **Return all patients:** Read `patient.json` and return all records from `GET /patients`.
3. **Get one patient:** Implement `GET /patients/{patient_id}` and return a `404` response for a missing ID.
4. **Create an about endpoint:** Add `GET /about` and return a short description of your API.
5. **Test with Swagger:** Open `/docs`, execute each endpoint, and inspect the response status and body.
6. **Add another patient:** Add a new valid object to `patient.json` and check that it appears in `/patients`.
7. **Try an invalid ID:** Request `/patients/abc` and observe FastAPI's validation response.

## 16. Video Links

The notes above cover foundational FastAPI concepts and the patient JSON API example. They are not a verified, exhaustive transcript of the exact lectures. To create exact timestamped notes, use the videos' transcripts or captions as source material.

- [Lecture 1 — YouTube](https://www.youtube.com/watch?v=WJKsPchji0Q&list=PLKnIA16_RmvZ41tjbKB2ZnwchfniNsMuQ&index=1)
- [Lecture 2 — YouTube](https://www.youtube.com/watch?v=lXx-_1r0Uss&list=PLKnIA16_RmvZ41tjbKB2ZnwchfniNsMuQ&index=2)

---

## Quick Revision

- FastAPI is used to build APIs in Python.
- `app = FastAPI()` creates the application.
- `@app.get("/")` registers a GET endpoint.
- Python dictionaries and lists can be returned as JSON responses.
- `patient.json` can be read with `json.load()`.
- `Path(__file__).resolve().parent` helps find files relative to the Python script.
- Path parameters can be declared with type hints, for example `patient_id: int`.
- `HTTPException` can return an error such as `404 Not Found`.
- `/docs` opens Swagger UI, and `/redoc` opens ReDoc.
- Use a virtual environment to isolate project dependencies.
"""

output_path = "/mnt/data/README.md"
pypandoc.convert_text(readme, "md", format="md", outputfile=output_path, extra_args=["--standalone"])
print(f"Created: {output_path}")
