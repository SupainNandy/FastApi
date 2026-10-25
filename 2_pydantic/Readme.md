
Pydantic Crash Course — FastAPI Notes

Beginner-friendly notes on Pydantic, Python data validation, and using Pydantic models with FastAPI.

> **Scope note:** These are study notes on the Pydantic concepts relevant to the CampusX FastAPI playlist. They are not a verified word-for-word transcript of the linked video.

## Table of Contents

1. [What is Pydantic?](#1-what-is-pydantic)
2. [Why Data Validation Matters](#2-why-data-validation-matters)
3. [Install Pydantic](#3-install-pydantic)
4. [Your First Pydantic Model](#4-your-first-pydantic-model)
5. [Validate Data](#5-validate-data)
6. [Type Conversion and Strict Validation](#6-type-conversion-and-strict-validation)
7. [Required and Optional Fields](#7-required-and-optional-fields)
8. [Default Values](#8-default-values)
9. [Field Constraints](#9-field-constraints)
10. [Nested Models and Lists](#10-nested-models-and-lists)
11. [Serialize a Model](#11-serialize-a-model)
12. [Use Pydantic with FastAPI](#12-use-pydantic-with-fastapi)
13. [Request and Response Models](#13-request-and-response-models)
14. [Common Validation Errors](#14-common-validation-errors)
15. [Pydantic v1 vs v2](#15-pydantic-v1-vs-v2)
16. [Interview Questions](#16-interview-questions)
17. [Practice Exercises](#17-practice-exercises)
18. [Video Link](#18-video-link)

## 1. What is Pydantic?

Pydantic is a Python library that uses type annotations to validate and parse data. It helps ensure that incoming data follows the structure and rules defined by your model.

In FastAPI, Pydantic is commonly used to validate request bodies and define the shape of API data.

For example, a patient record may require:

- `name`: string
- `age`: integer
- `city`: string
- `height`: positive number

A Pydantic model describes these fields and validates supplied data.

## 2. Why Data Validation Matters

Imagine an API expects a patient's age as an integer, but receives `"twenty"` instead.

Without validation, invalid data may cause bugs later in the application. Validation lets the application detect data that does not meet the expected schema.

Pydantic helps with:

- Checking required fields.
- Checking data types.
- Applying constraints such as minimum and maximum values.
- Producing structured validation errors.
- Converting valid data into Python objects.
- Serializing model data to dictionaries or JSON.

**Important:** Validation checks data against the rules you define. It does not automatically prove that the data is true or medically correct.

## 3. Install Pydantic

Activate your project's virtual environment, then run:

```bash
pip install pydantic
```

For FastAPI projects, install the framework and its standard dependencies as well:

```bash
pip install "fastapi[standard]"
```

## 4. Your First Pydantic Model

Create a file named `pydantic_demo.py`:

```python
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
    city: str

student = Student(
    name="Rahul",
    age=22,
    city="Kolkata"
)

print(student)
print(student.name)
print(student.age)
```

### Explanation

- `BaseModel` is the base class used to define a Pydantic model.
- `Student` is a model that describes the expected student data.
- `name: str` means the field is expected to be a string.
- `age: int` means the field is expected to be an integer.
- `Student(...)` creates an instance and validates the provided data.
- `student.name` accesses the value of the `name` field.

A model instance is a Python object, not just a dictionary.

## 5. Validate Data

### Valid input

```python
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int

student = Student(name="Priya", age=21)

print(student.name)
print(student.age)
```

Output:

```text
Priya
21
```

### Invalid input

```python
from pydantic import BaseModel, ValidationError

class Student(BaseModel):
    name: str
    age: int

try:
    student = Student(name="Priya", age="twenty")
except ValidationError as error:
    print(error)
```

Pydantic raises a `ValidationError` because `"twenty"` cannot be parsed as an integer.

In real applications, handle validation errors appropriately rather than letting them crash a script unexpectedly.

## 6. Type Conversion and Strict Validation

Depending on the field type and input, Pydantic may convert compatible values into the expected type.

For example, in normal (non-strict) validation, a numeric string such as `"21"` may be parsed as an integer:

```python
from pydantic import BaseModel

class Student(BaseModel):
    age: int

student = Student(age="21")
print(student.age)
print(type(student.age))
```

The parsed value is an integer.

However, not every value can be converted. `"twenty"` cannot become an integer.

### Strict validation

If you do not want Pydantic to coerce values, use strict types or strict configuration where appropriate.

```python
from pydantic import BaseModel, ConfigDict

class Student(BaseModel):
    model_config = ConfigDict(strict=True)

    age: int
```

With strict validation, a string `"21"` is not accepted as an integer field value.

Choose strictness based on your API's requirements.

## 7. Required and Optional Fields

A field without a default value is required.

```python
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
```

Both `name` and `age` must be supplied.

### A field that can contain `None`

```python
class Student(BaseModel):
    name: str
    nickname: str | None
```

In Pydantic v2, `nickname` is still required, but its value may be a string or `None`.

To make it optional to omit, provide a default:

```python
class Student(BaseModel):
    name: str
    nickname: str | None = None
```

Now `nickname` can be omitted and defaults to `None`.

**Remember:**
- `str | None` means the value can be a string or `None`.
- `= None` supplies a default, so the field may be omitted.

## 8. Default Values

You can assign default values to fields.

```python
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    country: str = "India"

student = Student(name="Amit")

print(student.country)
```

Output:

```text
India
```

Because `country` has a default value, the caller does not need to provide it.

For mutable defaults such as lists or dictionaries, Pydantic handles model field defaults safely. For clarity, you can also use `Field(default_factory=...)`.

```python
from pydantic import BaseModel, Field

class Student(BaseModel):
    skills: list[str] = Field(default_factory=list)
```

## 9. Field Constraints

Use `Field` to define constraints and metadata for fields.

```python
from pydantic import BaseModel, Field

class Patient(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=0, le=120)
    height_cm: float = Field(gt=0)
```

Meaning:

- `min_length=2`: string must contain at least two characters.
- `max_length=50`: string must contain no more than 50 characters.
- `ge=0`: age must be greater than or equal to zero.
- `le=120`: age must be less than or equal to 120.
- `gt=0`: height must be greater than zero.

Common constraint keywords:

| Constraint | Meaning |
|---|---|
| `gt` | Greater than |
| `ge` | Greater than or equal to |
| `lt` | Less than |
| `le` | Less than or equal to |
| `min_length` | Minimum string length |
| `max_length` | Maximum string length |
| `pattern` | String must match a regular expression |

Example:

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(min_length=2)
    price: float = Field(gt=0)
```

## 10. Nested Models and Lists

Pydantic models can contain other models and lists.

```python
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name: str
    age: int
    address: Address
    skills: list[str]

student = Student(
    name="Rahul",
    age=22,
    address={
        "city": "Kolkata",
        "country": "India"
    },
    skills=["Python", "FastAPI"]
)

print(student.address.city)
print(student.skills)
```

Pydantic validates nested structures as well as top-level fields.

This is useful when an API accepts complex JSON data.

## 11. Serialize a Model

Serialization means converting a model into a format suitable for storage or transmission.

With Pydantic v2:

```python
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int

student = Student(name="Priya", age=21)

# Convert to a Python dictionary
student_dict = student.model_dump()
print(student_dict)

# Convert to a JSON string
student_json = student.model_dump_json()
print(student_json)
```

Use:

- `model_dump()` to get a Python dictionary.
- `model_dump_json()` to get a JSON string.

These methods are useful when preparing data for APIs, logs, or storage.

## 12. Use Pydantic with FastAPI

FastAPI uses Pydantic models to validate request bodies.

Create `main.py`:

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Student(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(ge=1, le=120)
    city: str

@app.post("/students")
def create_student(student: Student):
    return {
        "message": "Student received successfully",
        "student": student
    }
```

Run the server:

```bash
fastapi dev main.py
```

Open:

```text
http://127.0.0.1:8000/docs
```

Select `POST /students`, click **Try it out**, and provide a request body such as:

```json
{
  "name": "Rahul",
  "age": 22,
  "city": "Kolkata"
}
```

FastAPI validates the request body using the `Student` model before calling the endpoint function.

If the request is invalid, FastAPI returns a validation error response instead of running the endpoint function normally.

## 13. Request and Response Models

Request models describe data the client is allowed to submit. Response models describe the shape of data returned by an endpoint.

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class StudentCreate(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(ge=1, le=120)

class StudentResponse(BaseModel):
    name: str
    age: int
    status: str

@app.post("/students", response_model=StudentResponse)
def create_student(student: StudentCreate):
    return {
        "name": student.name,
        "age": student.age,
        "status": "created",
        "internal_note": "This extra field is not part of the response model"
    }
```

The `response_model` tells FastAPI to validate and filter the response to the declared schema. In this example, `internal_note` is not included in the output.

Separate request and response models are useful when the server should not expose internal fields or when the request schema differs from the response schema.

## 14. Common Validation Errors

| Problem | What it means |
|---|---|
| Missing required field | A required field was not supplied |
| Wrong data type | A value cannot be validated or parsed as the expected type |
| Value below minimum | A numeric value violates a lower bound |
| Value above maximum | A numeric value violates an upper bound |
| String too short | The string does not meet `min_length` |
| String too long | The string exceeds `max_length` |
| Invalid nested data | A nested object or list item does not match its model |

FastAPI typically returns HTTP `422 Unprocessable Entity` for request data that fails validation. The response contains details identifying the fields and validation issues.

## 15. Pydantic v1 vs v2

Use the version installed in your project and consult its matching documentation.

| Task | Pydantic v1 | Pydantic v2 |
|---|---|---|
| Convert model to dictionary | `.dict()` | `.model_dump()` |
| Convert model to JSON string | `.json()` | `.model_dump_json()` |
| Parse and validate an object | `.parse_obj(data)` | `.model_validate(data)` |
| Model configuration | Inner `Config` class | `model_config = ConfigDict(...)` |

For new projects, examples should generally use Pydantic v2 unless a dependency requires v1.

## 16. Interview Questions

### Q1. What is Pydantic?

Pydantic is a Python library that validates and parses data using type annotations and model definitions.

### Q2. What is `BaseModel`?

`BaseModel` is the base class used to define Pydantic models and validate their fields.

### Q3. Why is Pydantic used with FastAPI?

It validates incoming request data, defines schemas, helps generate API documentation, and supports consistent data handling.

### Q4. What happens when required data is missing?

Pydantic raises a validation error. In a FastAPI request, the framework normally returns a validation response and does not call the endpoint function with invalid input.

### Q5. What is the difference between `str | None` and `str | None = None`?

`str | None` permits a string or `None` but is required in Pydantic v2 if no default is provided. Adding `= None` makes the field omittable and gives it a default value.

### Q6. What is `Field()` used for?

`Field()` provides constraints, defaults, and metadata for model fields.

### Q7. What is the difference between `model_dump()` and `model_dump_json()`?

`model_dump()` returns a Python dictionary. `model_dump_json()` returns a JSON-formatted string.

### Q8. What is a nested model?

A nested model is a Pydantic model used as a field inside another model, allowing structured data to be validated at multiple levels.

### Q9. What does `response_model` do in FastAPI?

It declares and validates the output schema and can filter fields that are not part of the response model.

### Q10. What is strict validation?

Strict validation reduces or prevents automatic type coercion, requiring inputs to match the expected types more closely.

## 17. Practice Exercises

1. Create a `Book` model with `title`, `author`, and `pages`.
2. Add constraints so `pages` must be greater than zero.
3. Create a `Patient` model with `name`, `age`, and `city`.
4. Make `age` required and constrain it to a reasonable range.
5. Create an `Address` model and nest it inside a `Patient` model.
6. Use `model_dump()` to convert a model into a dictionary.
7. Create a FastAPI `POST /patients` endpoint that accepts a `Patient` model.
8. Submit valid and invalid JSON through `/docs` and compare the responses.
9. Define a response model that excludes an internal field.
10. Try strict validation and observe how string numbers are handled.

## 18. Video Link

- [Pydantic Crash Course — CampusX (Playlist video 5)](https://www.youtube.com/watch?v=lRArylZCeOs&list=PLKnIA16_RmvZ41tjbKB2ZnwchfniNsMuQ&index=5)
- [CampusX FastAPI course notes preview](https://learnwith.campusx.in/s/preview/courses/FastAPI-1762939168928)

---

## Quick Revision

- Pydantic validates and parses data based on model definitions and type annotations.
- Create models by inheriting from `BaseModel`.
- Fields without defaults are required.
- Use `Field()` for constraints such as minimum values and string length.
- Pydantic supports nested models and typed lists.
- In Pydantic v2, use `model_dump()` for dictionaries and `model_dump_json()` for JSON strings.
- FastAPI validates request bodies declared with Pydantic models.
- `response_model` defines the expected output schema.
- FastAPI typically returns a `422` response when request data fails validation.
'''

output_path = "/mnt/data/README_Pydantic_Crash_Course.md"
pypandoc.convert_text(readme, "md", format="md", outputfile=output_path, extra_args=["--standalone"])
print(f"Created: {output_path}")
