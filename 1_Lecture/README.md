# FastAPI — Beginner's Guide

A beginner-friendly guide to learning FastAPI with simple Python examples, validation techniques, and API development concepts.

## Table of Contents

1. [What is FastAPI?](#1-what-is-fastapi)
2. [Create Your First API](#2-create-your-first-api)
3. [HTTP Methods](#3-http-methods)
4. [Path Parameters](#4-path-parameters)
5. [Path() Validation](#5-path-validation)
6. [Query Parameters](#6-query-parameters)
7. [Query() Validation](#7-query-validation)
8. [Request Body with Pydantic](#8-request-body-with-pydantic)
9. [Optional Parameters](#9-optional-parameters)
10. [Response Models](#10-response-models)
11. [HTTPException](#11-httpexception)
12. [Status Codes](#12-status-codes)
13. [Automatic API Documentation](#13-automatic-api-documentation)
14. [Async and Await](#14-async-and-await)
15. [Routers](#15-routers)
16. [Middleware](#16-middleware)
17. [CORS](#17-cors)
18. [Dependency Injection](#18-dependency-injection)
19. [Environment Variables](#19-environment-variables)
20. [Database Integration](#20-database-integration)
21. [Recommended Learning Roadmap](#21-recommended-learning-roadmap)

---

## 1. What is FastAPI?

FastAPI is a modern Python framework used to build APIs. It provides automatic data validation, asynchronous support, and interactive API documentation.

### Install Dependencies

```bash
pip install fastapi uvicorn
```

## 2. Create Your First API

Create a file named `main.py`.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI"}
```

### Run the Application

```bash
uvicorn main:app --reload
```

- `main` — Python filename (`main.py`).
- `app` — FastAPI application object.
- `--reload` — restarts the server automatically when code changes.

Open: `http://127.0.0.1:8000`

---

## 3. HTTP Methods

HTTP methods define the action an API performs.

| Method | Purpose |
|---|---|
| `GET` | Retrieve data |
| `POST` | Create data |
| `PUT` | Replace or update a resource |
| `PATCH` | Partially update a resource |
| `DELETE` | Delete a resource |

### Example

```python
@app.get("/users")
def get_users():
    return {"message": "Get users"}

@app.post("/users")
def create_user():
    return {"message": "User created"}

@app.put("/users/1")
def update_user():
    return {"message": "User updated"}

@app.delete("/users/1")
def delete_user():
    return {"message": "User deleted"}
```

These are basic examples; they return messages rather than performing database operations.

---

## 4. Path Parameters

Path parameters pass values directly through the URL to identify a particular resource.

### Example

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

**Request URL:**

`http://127.0.0.1:8000/users/10`

**Output:**

```json
{
  "user_id": 10
}
```

### Key Points

- `{user_id}` defines a path parameter.
- `user_id: int` specifies its data type.
- FastAPI automatically converts and validates the value.

---

## 5. Path() Validation

`Path()` adds validation rules and documentation to path parameters.

### Example

```python
from fastapi import Path

@app.get("/products/{product_id}")
def get_product(
    product_id: int = Path(
        ...,
        gt=0,
        description="The ID of the product"
    )
):
    return {"product_id": product_id}
```

**Valid URL:**

`http://127.0.0.1:8000/products/10`

**Invalid URL:**

`http://127.0.0.1:8000/products/0`

The second request returns a validation error because the ID must be greater than zero.

### Common Path() Arguments

| Argument | Meaning |
|---|---|
| `...` | Parameter is required |
| `gt=0` | Greater than 0 |
| `ge=1` | Greater than or equal to 1 |
| `lt=100` | Less than 100 |
| `le=100` | Less than or equal to 100 |
| `description` | Adds a description to API documentation |

**Remember:** Path parameters are required because they are part of the URL path.

---

## 6. Query Parameters

Query parameters pass additional values through the URL, usually for filtering, searching, sorting, or pagination.

They appear after `?` in the URL.

### Example

```python
@app.get("/products")
def get_products(
    category: str = "all",
    limit: int = 10
):
    return {
        "category": category,
        "limit": limit
    }
```

**Request URL:**

`http://127.0.0.1:8000/products?category=books&limit=5`

**Output:**

```json
{
  "category": "books",
  "limit": 5
}
```

Here, `category` and `limit` are query parameters with default values.

---

## 7. Query() Validation

`Query()` adds validation rules and documentation to query parameters.

### Example

```python
from fastapi import Query

@app.get("/search")
def search_products(
    search: str = Query(
        ...,
        min_length=3,
        max_length=20,
        description="Search products by name"
    )
):
    return {
        "search": search,
        "message": "Products fetched successfully"
    }
```

**Valid URL:**

`http://127.0.0.1:8000/search?search=laptop`

**Output:**

```json
{
  "search": "laptop",
  "message": "Products fetched successfully"
}
```

**Invalid URL:**

`http://127.0.0.1:8000/search?search=ab`

FastAPI returns a validation error because the search value contains fewer than three characters.

### Common Query() Arguments

| Argument | Meaning |
|---|---|
| `...` | Parameter is required |
| `min_length=3` | Minimum string length |
| `max_length=20` | Maximum string length |
| `gt=0` | Value must be greater than 0 |
| `ge=1` | Value must be greater than or equal to 1 |
| `description` | Describes the parameter |
| `pattern="^[a-z]+$"` | Validates a string against a regular expression |

### Optional Query Parameter

```python
@app.get("/product-search")
def search_products(
    search: str | None = Query(
        default=None,
        min_length=3
    )
):
    return {"search": search}
```

Both requests are valid:

- `/product-search`
- `/product-search?search=laptop`

The first request returns `{"search": null}`.

### Path() vs Query()

| Feature | `Path()` | `Query()` |
|---|---|---|
| Value comes from | URL path | URL query string |
| Example | `/users/10` | `/users?id=10` |
| Common use | Identify a resource | Search or filter results |
| Validation | Yes | Yes |

---

## 8. Request Body with Pydantic

A request body sends data to an API, commonly when creating or updating a resource.

Pydantic models define the expected data structure and validate incoming values.

### Example

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str

@app.post("/users")
def create_user(user: User):
    return {
        "message": "User created",
        "user": user
    }
```

**Example JSON Request Body:**

```json
{
  "name": "Rahul",
  "age": 25,
  "email": "rahul@example.com"
}
```

FastAPI validates the incoming data automatically.

---

## 9. Optional Parameters

Optional parameters allow users to omit a value from a request.

### Example

```python
@app.get("/user-search")
def search_user(name: str | None = None):
    return {"name": name}
```

**Example URLs:**

- `/user-search?name=Rahul`
- `/user-search`

The second request returns:

```json
{
  "name": null
}
```

Here, `None` is the default value, and `str | None` allows either a string or `None`.

---

## 10. Response Models

`response_model` defines and validates the structure of the response returned by an endpoint.

### Example

```python
from pydantic import BaseModel

class UserResponse(BaseModel):
    name: str
    age: int

@app.get("/user", response_model=UserResponse)
def get_user():
    return {
        "name": "Rahul",
        "age": 25,
        "password": "secret"
    }
```

**Output:**

```json
{
  "name": "Rahul",
  "age": 25
}
```

The extra `password` field is excluded from the response.

**Important:** Response models help control API output and prevent unintended fields from being exposed.

---

## 11. HTTPException

`HTTPException` returns an HTTP error when a request cannot be completed.

### Example

```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "user_id": user_id,
        "name": "Rahul"
    }
```

- `/users/1` returns the user.
- `/users/2` returns a `404 Not Found` error.

### Common Error Status Codes

| Code | Meaning |
|---|---|
| `400` | Bad Request |
| `401` | Unauthorized |
| `403` | Forbidden |
| `404` | Not Found |
| `422` | Validation Error |
| `500` | Internal Server Error |

---

## 12. Status Codes

Status codes indicate the result of an HTTP request.

### Example

```python
from fastapi import status

@app.post(
    "/items",
    status_code=status.HTTP_201_CREATED
)
def create_item():
    return {"message": "Item created"}
```

The API returns status code `201 Created`.

### Common Status Codes

| Code | Meaning |
|---|---|
| `200` | OK |
| `201` | Created |
| `204` | No Content |
| `400` | Bad Request |
| `401` | Unauthorized |
| `403` | Forbidden |
| `404` | Not Found |
| `422` | Validation Error |
| `500` | Internal Server Error |

---

## 13. Automatic API Documentation

FastAPI automatically generates interactive API documentation.

Start the server and open the following URLs:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

You can inspect endpoints, view request and response schemas, and test API requests directly in your browser.

---

## 14. Async and Await

`async def` allows you to create asynchronous endpoints. It is useful for I/O operations when working with compatible asynchronous libraries.

### Example

```python
@app.get("/hello")
async def hello():
    return {"message": "Hello, FastAPI"}
```

Use `async def` with asynchronous operations. Normal `def` is also valid for regular endpoints.

**Important:** Declaring a function `async` does not automatically make blocking operations non-blocking.

---

## 15. Routers

`APIRouter` helps organize endpoints into separate files as a project grows.

### users.py

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def get_users():
    return [
        {"id": 1, "name": "Rahul"}
    ]
```

### main.py

```python
from fastapi import FastAPI
from users import router

app = FastAPI()

app.include_router(router)
```

Now `/users` is available through the main application.

**Benefit:** Routers keep your code organized and easier to maintain.

---

## 16. Middleware

Middleware runs around requests and responses. It is useful for request timing, logging, and other shared operations.

### Example

```python
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time(
    request: Request,
    call_next
):
    start = time.time()

    response = await call_next(request)

    process_time = time.time() - start
    response.headers["X-Process-Time"] = str(process_time)

    return response
```

This example adds an `X-Process-Time` header containing the request processing duration in seconds.

---

## 17. CORS

CORS stands for Cross-Origin Resource Sharing. It controls which browser-based frontend origins can access your API.

### Example

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

Replace the example origin with your actual frontend URL.

**Security tip:** Avoid allowing every origin in production unless it is genuinely required.

---

## 18. Dependency Injection

`Depends()` allows FastAPI to provide reusable dependencies to endpoints.

Dependencies are useful for authentication, database sessions, and shared logic.

### Example

```python
from fastapi import Depends

def common_params(limit: int = 10):
    return {"limit": limit}

@app.get("/items")
def get_items(
    params: dict = Depends(common_params)
):
    return params
```

**Request URL:**

`http://127.0.0.1:8000/items?limit=5`

**Output:**

```json
{
  "limit": 5
}
```

FastAPI calls `common_params()` and passes its result to the endpoint.

---

## 19. Environment Variables

Environment variables store configuration outside your source code, including application settings and database connection details.

### Install

```bash
pip install python-dotenv
```

### .env

```env
APP_NAME=My FastAPI App
```

### main.py

```python
import os
from dotenv import load_dotenv

load_dotenv()

app_name = os.getenv("APP_NAME", "FastAPI")

app = FastAPI(title=app_name)
```

### .gitignore

```gitignore
.env
myenv/
__pycache__/
*.pyc
```

**Security tip:** Never commit passwords, API keys, tokens, or other secrets to GitHub.

---

## 20. Database Integration

FastAPI can connect to databases such as PostgreSQL, MySQL, and SQLite through appropriate database libraries.

### Typical Database Workflow

1. Receive a request.
2. Validate the incoming data.
3. Perform a database operation.
4. Return the result.

### Common Database Tools

| Tool | Purpose |
|---|---|
| PostgreSQL | Relational database |
| MySQL | Relational database |
| SQLite | Lightweight database |
| SQLAlchemy | Python ORM and SQL toolkit |
| SQLModel | SQL database library built on Pydantic and SQLAlchemy |

A production application should manage database sessions and connections correctly and keep credentials in environment variables.

---

## 21. Recommended Learning Roadmap

Follow this order to build a strong foundation in FastAPI.

- [ ] Install Python, FastAPI, and Uvicorn.
- [ ] Create your first API.
- [ ] Learn HTTP methods.
- [ ] Practice path parameters.
- [ ] Understand `Path()` validation.
- [ ] Learn query parameters.
- [ ] Understand `Query()` validation.
- [ ] Validate request bodies with Pydantic.
- [ ] Learn optional parameters and response models.
- [ ] Handle errors using `HTTPException`.
- [ ] Understand HTTP status codes.
- [ ] Organize endpoints using `APIRouter`.
- [ ] Learn dependency injection and middleware.
- [ ] Configure CORS and environment variables.
- [ ] Connect PostgreSQL.
- [ ] Implement CRUD operations.
- [ ] Learn authentication and authorization.
- [ ] Write API tests using `pytest` and FastAPI's `TestClient`.

---

## Practice Project: Patient Management API

Build a Patient Management API to practice the concepts covered in this guide.

### Suggested Features

- Create a patient.
- Retrieve all patients.
- Retrieve a patient by ID.
- Search patients by name.
- Filter patients by city.
- Update patient details.
- Delete a patient.
- Validate patient data using Pydantic.
- Store patient records in PostgreSQL.

Start with an in-memory Python list, then connect PostgreSQL when you understand the fundamentals.

---

## Useful Resources

- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [Python Official Documentation](https://docs.python.org/3/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Learning tip:** Practice each concept by creating a small endpoint and testing it at `/docs`. Understanding how requests, validation, and responses work is more useful than memorizing syntax.
