# FastAPI — Beginner's Guide

A beginner-friendly guide to learning FastAPI with simple Python examples.

## 1. What is FastAPI?

FastAPI is a modern Python framework used to build REST APIs. It supports automatic data validation, high performance, and interactive API documentation.

**Install dependencies:**

```bash
pip install fastapi uvicorn
```

## 2. Create Your First API

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI"}
```

Run the application:

```bash
uvicorn main:app --reload
```

- `main` — Python filename (`main.py`).
- `app` — FastAPI application object.
- `--reload` — automatically restarts the server when code changes.

Open: `http://127.0.0.1:8000`

## 3. HTTP Methods

HTTP methods define what action an API performs.

| Method | Purpose |
|---|---|
| `GET` | Retrieve data |
| `POST` | Create data |
| `PUT` | Replace or update data |
| `PATCH` | Partially update data |
| `DELETE` | Delete data |

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

## 4. Path Parameters

Path parameters pass values directly through the URL.

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

**Example URL:**

`http://127.0.0.1:8000/users/10`

**Output:**

```json
{
  "user_id": 10
}
```

FastAPI converts the value to an integer and validates its type.

## 5. Path() Validation

`Path()` adds validation and documentation to path parameters.

```python
from fastapi import Path

@app.get("/products/{product_id}")
def get_product(
    product_id: int = Path(..., gt=0)
):
    return {"product_id": product_id}
```

- `...` — parameter is required.
- `gt=0` — value must be greater than zero.

A request to `/products/0` returns a validation error.

## 6. Query Parameters

Query parameters filter or customize a request. They appear after `?` in the URL.

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

**Example URL:**

`http://127.0.0.1:8000/products?category=books&limit=5`

**Output:**

```json
{
  "category": "books",
  "limit": 5
}
```

Here, `category` and `limit` are query parameters with default values.

## 7. Request Body with Pydantic

A request body sends data to an API, commonly when creating a resource. Pydantic models define and validate the expected data.

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

**Example JSON request body:**

```json
{
  "name": "Rahul",
  "age": 25,
  "email": "rahul@example.com"
}
```

FastAPI validates the request body automatically.

## 8. Optional Parameters

Optional parameters allow a value to be omitted.

```python
@app.get("/search")
def search_user(name: str | None = None):
    return {"name": name}
```

**Example URLs:**

- `/search?name=Rahul`
- `/search`

The second request returns `{"name": null}`.

## 9. Response Models

`response_model` defines the structure of the response returned by an endpoint.

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

The extra `password` field is excluded from the response. Response models help control and validate API output.

## 10. HTTPException

`HTTPException` returns an HTTP error when a request cannot be completed.

```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {"user_id": user_id, "name": "Rahul"}
```

- `404` — resource not found.
- `400` — bad request.
- `401` — authentication required or failed.
- `403` — access forbidden.

Use the status code that correctly represents the error.

## 11. Status Codes

Status codes describe the result of an HTTP request.

```python
from fastapi import status

@app.post(
    "/items",
    status_code=status.HTTP_201_CREATED
)
def create_item():
    return {"message": "Item created"}
```

Common codes:

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

## 12. Automatic API Documentation

FastAPI automatically generates interactive API documentation.

After starting your server, visit:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

You can inspect endpoints, view schemas, and test requests directly in your browser.

## 13. Async and Await

`async def` allows you to define asynchronous endpoints. It is especially useful for I/O operations when used with compatible asynchronous libraries.

```python
@app.get("/hello")
async def hello():
    return {"message": "Hello, FastAPI"}
```

Use `async def` with asynchronous operations. Normal `def` is also perfectly valid for regular endpoints.

## 14. Routers

`APIRouter` helps organize endpoints into separate files as a project grows.

**users.py**

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def get_users():
    return [{"id": 1, "name": "Rahul"}]
```

**main.py**

```python
from fastapi import FastAPI
from users import router

app = FastAPI()
app.include_router(router)
```

Now `/users` is available through the main application.

## 15. Middleware

Middleware runs around requests and responses. It is useful for logging, timing, and other cross-cutting tasks.

```python
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(
        time.time() - start
    )
    return response
```

This example adds an `X-Process-Time` header containing the request processing duration in seconds.

## 16. CORS

CORS controls which browser-based frontend origins can access your API.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Replace the example origin with your actual frontend URL. Avoid allowing every origin in production unless it is genuinely required.

## 17. Dependency Injection

`Depends()` lets FastAPI provide reusable dependencies to endpoints.

```python
from fastapi import Depends

def common_params(limit: int = 10):
    return {"limit": limit}

@app.get("/items")
def get_items(params: dict = Depends(common_params)):
    return params
```

The endpoint receives the result of `common_params()` through dependency injection. Dependencies are useful for authentication, database sessions, and reusable logic.

## 18. Environment Variables

Environment variables keep configuration, such as secrets and database URLs, outside your source code.

Install:

```bash
pip install python-dotenv
```

**.env**

```env
APP_NAME=My FastAPI App
```

**main.py**

```python
import os
from dotenv import load_dotenv

load_dotenv()

app_name = os.getenv("APP_NAME", "FastAPI")
```

Add `.env` to `.gitignore`. Never commit passwords, tokens, or other secrets to GitHub.

## 19. Database Integration

FastAPI can work with databases such as PostgreSQL, MySQL, and SQLite using appropriate drivers and libraries.

A typical database-backed API follows this flow:

1. Receive a request.
2. Validate the incoming data.
3. Perform a database operation.
4. Return the result.

Common choices include SQLAlchemy or SQLModel for ORM-based applications. Use a database session or connection lifecycle that is managed correctly.

## 20. Recommended Learning Order

- [ ] Install FastAPI and Uvicorn.
- [ ] Create your first API.
- [ ] Learn HTTP methods.
- [ ] Practice path parameters and `Path()`.
- [ ] Learn query parameters.
- [ ] Validate request bodies using Pydantic.
- [ ] Learn response models and status codes.
- [ ] Handle errors with `HTTPException`.
- [ ] Organize endpoints using `APIRouter`.
- [ ] Learn dependencies and middleware.
- [ ] Connect PostgreSQL.
- [ ] Learn authentication and testing.

## Useful Resources

- Official documentation: https://fastapi.tiangolo.com/
- Python documentation: https://docs.python.org/3/
- Pydantic documentation: https://docs.pydantic.dev/

---

**Practice project idea:** Build a Patient Management API with endpoints to create, retrieve, update, and delete patient records. Start with a Python list or JSON file, then connect PostgreSQL when you're comfortable with the fundamentals.
