# Python Data Validation and Pydantic — Learning Notes

> **Today's learning:** Python type hints, manual validation, Pydantic models, field constraints, field and model validators, computed fields, nested models, and `model_dump()`.

These notes use patient data as a learning example. The functions that print “inserted” or “updated” do **not** connect to a real database.

## Table of Contents

1. [Python Dynamic Typing](#1-python-dynamic-typing)
2. [Type Hints](#2-type-hints)
3. [Manual Type Validation](#3-manual-type-validation)
4. [Data Validation](#4-data-validation)
5. [Introduction to Pydantic](#5-introduction-to-pydantic)
6. [Installing Pydantic](#6-installing-pydantic)
7. [Creating a Pydantic Model](#7-creating-a-pydantic-model)
8. [Field Constraints and Metadata](#8-field-constraints-and-metadata)
9. [Optional Fields and Collections](#9-optional-fields-and-collections)
10. [Field Validators](#10-field-validators)
11. [Model Validators](#11-model-validators)
12. [Computed Fields](#12-computed-fields)
13. [Nested Models](#13-nested-models)
14. [Serializing Models with `model_dump()`](#14-serializing-models-with-model_dump)
15. [Important Corrections and Common Mistakes](#15-important-corrections-and-common-mistakes)
16. [Quick Revision](#16-quick-revision)
17. [Practice Exercises](#17-practice-exercises)

---

## 1. Python Dynamic Typing

Python is dynamically typed. A variable's type is determined at runtime, and a function without validation can receive values of unexpected types.

```python
def insert_patient_data(name, age):
    print("Name:", name)
    print("Age:", age)
    print("Data processed successfully.")

insert_patient_data("Ram", "Rupam")  # Runs without a type error
```

Python does not automatically reject `"Rupam"` for the `age` argument. An error may occur later if the function performs an operation that is incompatible with the value.

**Key point:** Dynamic typing does not mean Python has no types. It means type checking is not generally enforced through function annotations at compile time.

## 2. Type Hints

Type hints document the expected types and help editors, static type checkers, and developers understand how code should be used.

```python
def insert_patient_data(name: str, age: int) -> None:
    print("Name:", name)
    print("Age:", age)

insert_patient_data("Ram", "Rupam")  # Python still allows this call
```

- `name: str` indicates that `name` is expected to be a string.
- `age: int` indicates that `age` is expected to be an integer.
- `-> None` indicates that the function is not intended to return a value.

**Important:** Python does not enforce ordinary type hints automatically at runtime. Tools such as Pyright and mypy can detect many type mismatches before execution. Pydantic can validate data at runtime.

## 3. Manual Type Validation

Use `isinstance()` when you want to check types yourself.

```python
def insert_patient_data(name: str, age: int) -> None:
    if not isinstance(name, str) or not isinstance(age, int):
        raise TypeError("Name must be a string and age must be an integer.")

    print("Name:", name)
    print("Age:", age)

insert_patient_data("Ram", 25)  # Valid
# insert_patient_data("Ram", "Rupam")  # Raises TypeError
```

`TypeError` is appropriate when a value has an inappropriate type for the operation or API.

### A Python detail: `bool` is a subclass of `int`

```python
isinstance(True, int)  # True
```

If a value must be an actual integer and not a Boolean, use `type(value) is int` or a suitable strict-validation approach.

## 4. Data Validation

Type validation checks the kind of value. Data validation checks whether the value satisfies the application's rules.

```python
def insert_patient_data(name: str, age: int) -> None:
    if not isinstance(name, str) or type(age) is not int:
        raise TypeError("Name must be a string and age must be an integer.")

    if not name.strip():
        raise ValueError("Name cannot be empty.")

    if age < 0:
        raise ValueError("Age cannot be negative.")

    print("Name:", name)
    print("Age:", age)
    print("Data processed successfully.")

insert_patient_data("Ram", 25)  # Valid
# insert_patient_data("   ", 25)  # Raises ValueError
# insert_patient_data("Ram", -9)  # Raises ValueError
```

- `TypeError`: the value has an unsuitable type.
- `ValueError`: the type may be suitable, but the value violates a rule.

This is manual validation. Pydantic can express many of these rules declaratively.

---

## 5. Introduction to Pydantic

[Pydantic](https://docs.pydantic.dev/latest/) is a Python library for parsing and validating data using Python type annotations.

It is commonly used with FastAPI to validate request bodies, configuration, and structured data.

A Pydantic model can:
- Validate required fields and their types.
- Parse compatible inputs into the declared types when permitted.
- Apply constraints such as minimum values and maximum lengths.
- Run custom field-level and model-level validation.
- Represent nested data.
- Serialize model data into Python dictionaries.

By default, Pydantic may coerce compatible values. Strict validation can be enabled when conversion should not be allowed.

## 6. Installing Pydantic

It is recommended to use a virtual environment rather than installing packages into a system-managed Python environment.

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate it on Linux or macOS
source .venv/bin/activate

# On Windows PowerShell, use:
# .venv\Scripts\Activate.ps1

# Install Pydantic
python -m pip install "pydantic[email]"
```

The `email` extra installs the dependency needed for `EmailStr` email validation.

Check the installed version:

```bash
python -c "import pydantic; print(pydantic.__version__)"
```

## 7. Creating a Pydantic Model

A class that inherits from `BaseModel` becomes a Pydantic model.

```python
from pydantic import BaseModel, EmailStr, AnyUrl

class Patient(BaseModel):
    name: str
    email: EmailStr
    linkedin_url: AnyUrl
    age: int
    weight: float
    married: bool

patient_data = {
    "name": "Nitesh",
    "email": "abc@gmail.com",
    "linkedin_url": "https://linkedin.com/in/example",
    "age": 22,
    "weight": 50.2,
    "married": False,
}

patient = Patient(**patient_data)
print(patient)
```

### What happens here?

1. `patient_data` is a regular Python dictionary.
2. `**patient_data` unpacks its key-value pairs into keyword arguments.
3. Pydantic validates the supplied values against the model fields.
4. If validation succeeds, a `Patient` instance is created.
5. If validation fails, Pydantic raises a `ValidationError`.

### Useful types

| Type | Purpose |
|---|---|
| `str` | Text |
| `int` | Integer |
| `float` | Floating-point number |
| `bool` | Boolean value |
| `EmailStr` | Email-format validation |
| `AnyUrl` | URL validation |
| `List[str]` / `list[str]` | A list of strings |
| `Dict[str, str]` / `dict[str, str]` | A dictionary with string keys and values |
| `Optional[str]` / `str \| None` | A string or `None` |

`EmailStr` and `AnyUrl` validate formats; they do not prove that an email inbox exists or that a URL is reachable.

## 8. Field Constraints and Metadata

Use `Field` to define constraints and document a model field. Use `Annotated` to attach metadata to a type.

```python
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr, AnyUrl

class Patient(BaseModel):
    name: Annotated[
        str,
        Field(
            max_length=50,
            title="Name of the patient",
            description="Enter a patient name with at most 50 characters.",
            examples=["Nitish", "Amit"],
        ),
    ]

    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=120)
    weight: Annotated[float, Field(gt=0, strict=True)]
```

### Common `Field` constraints

| Constraint | Meaning |
|---|---|
| `gt=0` | Greater than zero |
| `ge=0` | Greater than or equal to zero |
| `lt=120` | Less than 120 |
| `le=100` | Less than or equal to 100 |
| `min_length=2` | Minimum length of 2 |
| `max_length=50` | Maximum length of 50 |
| `strict=True` | Disallow certain automatic type conversions for that field |
| `title` | Human-readable field title |
| `description` | Explanation of the field |
| `examples` | Example values for documentation |

`Annotated[type, Field(...)]` attaches field metadata to a type. You can also use assignment syntax such as `age: int = Field(gt=0, lt=120)`.

**Strict mode example:** with `weight: Annotated[float, Field(gt=0, strict=True)]`, a string such as `"50.2"` is rejected rather than converted to a float. A numeric float such as `50.2` is accepted.

## 9. Optional Fields and Collections

### Lists and dictionaries

```python
from typing import Optional
from pydantic import BaseModel, Field

class Patient(BaseModel):
    allergies: list[str] = Field(default_factory=list, max_length=5)
    contact_details: dict[str, str] | None = None
    nickname: Optional[str] = None
```

- `list[str]` means a list whose items should be strings.
- `dict[str, str]` means a dictionary with string keys and string values.
- `str | None` and `Optional[str]` mean the value can be a string or `None`.
- `default_factory=list` creates an empty list when no value is supplied.
- `max_length=5` limits the number of items in the list in this example.

### Required versus optional

In Pydantic v2, `Optional[str]` allows `None`, but does **not** by itself make a field optional to omit. Give it a default to make it omittable:

```python
class Example(BaseModel):
    required_but_nullable: str | None
    optional_name: str | None = None
```

`required_but_nullable` must be supplied, though its value can be `None`. `optional_name` may be omitted.

## 10. Field Validators

Use `@field_validator` to apply custom validation or transformation to one or more fields.

```python
from pydantic import BaseModel, EmailStr, field_validator

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, value: EmailStr) -> EmailStr:
        allowed_domains = {"hdfc.com", "icici.com"}
        domain = str(value).rsplit("@", 1)[-1].lower()

        if domain not in allowed_domains:
            raise ValueError("Email domain must be hdfc.com or icici.com")

        return value

    @field_validator("name")
    @classmethod
    def uppercase_name(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("age", mode="before")
    @classmethod
    def validate_age_input(cls, value):
        # Validate the raw input before Pydantic parses it as an integer.
        if type(value) is not int:
            raise ValueError("Age must be an integer")

        if not 1 <= value <= 99:
            raise ValueError("Age must be between 1 and 99")

        return value

patient = Patient(
    name=" nitesh ",
    email="abc@hdfc.com",
    age=30,
)

print(patient.name)  # NITESH
```

### Validator concepts

- `@field_validator("name")`: runs custom validation for the `name` field.
- `@classmethod`: declares the validator as a class method.
- `mode="before"`: receives the raw input before normal field parsing and validation.
- Default mode (`"after"`): runs after the field has been parsed and validated.
- Return the validated or transformed value.
- Raise `ValueError` when the value should be rejected.

**Note:** A domain allowlist is an application-specific rule, not general email-format validation. `EmailStr` checks the format; the custom validator restricts which domains are accepted.

## 11. Model Validators

Use `@model_validator` when a rule depends on multiple fields or the model as a whole.

```python
from pydantic import BaseModel, EmailStr, model_validator

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    contact_details: dict[str, str]

    @model_validator(mode="after")
    def require_emergency_contact_for_older_patients(self):
        if (
            self.age > 60
            and not self.contact_details.get("emergency", "").strip()
        ):
            raise ValueError(
                "Emergency contact is required for patients over 60."
            )

        return self
```

Example valid data:

```python
patient = Patient(
    name="John Doe",
    email="john@example.com",
    age=67,
    contact_details={
        "phone": "1234567890",
        "emergency": "9876543210",
    },
)
```

### `mode="after"` versus `mode="before"`

- **After:** receives the validated model instance (`self` in the example). Use it for rules involving parsed field values.
- **Before:** receives the raw input data, which may be a dictionary or another input form. Use it when you need to inspect or normalize input before field validation.

An after model validator should return the validated instance (`self`).

## 12. Computed Fields

A computed field exposes a value calculated from other model fields. The value does not need to be supplied by the caller.

```python
from pydantic import BaseModel, EmailStr, computed_field, Field

class Patient(BaseModel):
    name: str
    email: EmailStr
    weight: float = Field(gt=0, description="Weight in kilograms")
    height: float = Field(gt=0, description="Height in metres")

    @computed_field
    @property
    def bmi(self) -> float:
        # BMI = weight in kilograms / (height in metres ** 2)
        return round(self.weight / (self.height ** 2), 2)

patient = Patient(
    name="John Doe",
    email="john@example.com",
    weight=70.5,
    height=1.75,
)

print(patient.bmi)
print(patient.model_dump())
```

For these values, BMI is approximately `23.02`.

**Important:** BMI is `weight / (height ** 2)`. Do not divide the result by `2` again. The `@computed_field` decorator allows the property to be included in serialization, such as `model_dump()`.

## 13. Nested Models

A nested model lets one Pydantic model contain another Pydantic model. This is useful for structured data such as a patient with an address.

```python
from pydantic import BaseModel, EmailStr

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    gender: str = "Male"
    address: Address

address_data = {
    "street": "123 Main St",
    "city": "Kolkata",
    "state": "WB",
    "zip_code": "700001",
}

patient_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 67,
    "address": address_data,
}

patient = Patient(**patient_data)

print(patient.name)
print(patient.address.city)
print(patient.address.zip_code)
```

Pydantic can parse the nested dictionary into an `Address` instance and validate its fields. You do not have to instantiate `Address` manually first, although you can.

### Accessing nested data

```python
print(patient.address)        # Address model instance
print(patient.address.city)   # Kolkata
```

The default gender value is `"Male"` because no `gender` value was provided.

## 14. Serializing Models with `model_dump()`

In Pydantic v2, `model_dump()` converts a model instance into a Python dictionary. Nested models are converted to nested dictionaries.

```python
all_data = patient.model_dump()

selected_data = patient.model_dump(
    include={"name", "email", "address"}
)

data_without_private_fields = patient.model_dump(
    exclude={"name", "email", "address"}
)

provided_fields_only = patient.model_dump(exclude_unset=True)

print(all_data)
print(selected_data)
print(data_without_private_fields)
print(provided_fields_only)
```

### Common `model_dump()` options

| Option | Purpose |
|---|---|
| `model_dump()` | Serialize all fields by default |
| `include={...}` | Keep only the specified fields |
| `exclude={...}` | Omit specified fields |
| `exclude_unset=True` | Omit fields that were not explicitly set during model creation |
| `exclude_defaults=True` | Omit fields whose current values equal their defaults |
| `exclude_none=True` | Omit fields whose values are `None` |
| `mode="json"` | Produce JSON-compatible Python values |
| `model_dump_json()` | Serialize the model to a JSON string |

### Understanding `exclude_unset=True`

Suppose the model has `gender: str = "Male"` and you do not pass `gender` when creating the patient.

```python
patient.model_dump(exclude_unset=True)
```

The `gender` field is omitted from this dump because it was not explicitly supplied. It still exists on the model, and `patient.gender` still returns `"Male"`.

### Python dictionary versus JSON string

```python
python_dict = patient.model_dump()
json_text = patient.model_dump_json()

print(type(python_dict))  # <class 'dict'>
print(type(json_text))    # <class 'str'>
```

Use `model_dump()` when you need a Python dictionary. Use `model_dump_json()` when you need a JSON-formatted string.

---

## 15. Important Corrections and Common Mistakes

### 1. A type hint does not enforce runtime types

```python
def example(age: int):
    print(age)

example("twenty")  # Python itself does not reject this annotation
```

Use manual checks, Pydantic, or another runtime-validation approach when enforcement is required.

### 2. `Optional` does not automatically provide a default

```python
# Required field that accepts None:
nickname: str | None

# Field that can be omitted:
nickname: str | None = None
```

### 3. Define Boolean defaults correctly

Use:

```python
married: bool = False
```

Avoid:

```python
married: bool = Annotated[bool, Field(default=None)]
```

The latter mixes a type alias with a field default and conflicts with the declared non-nullable Boolean type. If the field can genuinely be unknown, use `married: bool | None = None`.

### 4. Validate values, not just their types

An integer age can still be invalid if it is negative or outside your application's allowed range. Use constraints such as `Field(gt=0, lt=120)` or a custom validator.

### 5. Correct BMI formula

```python
bmi = weight / (height ** 2)
```

Weight is in kilograms and height is in metres. Do not divide by `2` after calculating the formula.

### 6. Use `Field` defaults appropriately

For a collection that should start empty, prefer:

```python
allergies: list[str] = Field(default_factory=list)
```

For a nullable field, use an explicit `None` default if omission is allowed:

```python
contact_details: dict[str, str] | None = None
```

### 7. Do not confuse validation with database operations

Creating a Pydantic model validates and parses data in memory. It does not automatically insert or update a database record.

### 8. Use the right validator for the job

- `field_validator`: validation or transformation of individual fields.
- `model_validator`: rules involving several fields or the whole model.
- `computed_field`: exposes a calculated property in serialization; it is not a validator.

---

## 16. Quick Revision

| Concept | Main purpose |
|---|---|
| Dynamic typing | Python determines types at runtime |
| Type hints | Document expected types and support static analysis |
| `isinstance()` | Manually check an object's type |
| `BaseModel` | Define a validated data model |
| `EmailStr` | Validate email format |
| `AnyUrl` | Validate URL format |
| `Field` | Declare constraints, defaults, and metadata |
| `Annotated` | Attach metadata to a type |
| `field_validator` | Validate or transform a field |
| `model_validator` | Validate rules across the model |
| `computed_field` | Expose a derived property |
| Nested model | Represent structured data inside another model |
| `model_dump()` | Convert a model into a Python dictionary |
| `model_dump_json()` | Convert a model into a JSON string |
| `exclude_unset=True` | Omit fields not explicitly supplied |

### The overall workflow

```text
Raw input
   ↓
Pydantic model receives data
   ↓
Field parsing and type validation
   ↓
Field constraints and custom validators
   ↓
Model-level validation
   ↓
Validated model instance
   ↓
Access fields, compute properties, or serialize with model_dump()
```

The exact order and behavior of validators depend on their mode and the model configuration.

## 17. Practice Exercises

Try these exercises to reinforce today's learning:

1. Create a `Patient` model with `name`, `age`, and `email`.
2. Make `age` greater than zero and less than 120.
3. Add a field validator that trims whitespace from `name`.
4. Restrict email addresses to a list of allowed domains.
5. Add an `Address` model and nest it inside `Patient`.
6. Require an emergency contact when the patient's age is greater than 60.
7. Add `height` and `weight`, then compute BMI using `@computed_field`.
8. Use `model_dump(include={...})` to return only the patient's name and email.
9. Compare `model_dump()`, `model_dump(exclude_unset=True)`, and `model_dump_json()`.
10. Test invalid values and inspect the resulting `ValidationError`.

---

## References

- [Pydantic Documentation](https://docs.pydantic.dev/latest/)
- [Pydantic Fields](https://docs.pydantic.dev/latest/concepts/fields/)
- [Pydantic Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [Pydantic Models](https://docs.pydantic.dev/latest/concepts/models/)
- [Pydantic Computed Fields](https://docs.pydantic.dev/latest/concepts/fields/#the-computed_field-decorator)

**Learning summary:** Python type hints communicate intent, while Pydantic validates structured data at runtime. Field and model validators enforce custom rules, computed fields derive values, nested models organize related data, and `model_dump()` serializes validated model data.
