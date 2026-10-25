# ============================================================
# 1. PROBLEM: Python supports Dynamic Typing
# ============================================================

def insert_patient_data(name, age):
    print("Name:", name)
    print("Age:", age)
    print("Data inserted into the database successfully.")


# Python allows incorrect argument types without raising an error.
# Because Python is dynamically typed, types are checked at runtime
# when operations require them.

# insert_patient_data("Ram", "Rupam")


# ============================================================
# 2. TYPE HINTING: Type hints do not enforce types automatically
# ============================================================

def insert_patient_data(name: str, age: int):
    print("Name:", name)
    print("Age:", age)
    print("Data inserted into the database successfully.")


# Type hints help developers and IDEs understand expected types.
# Python does not automatically enforce these hints at runtime.

# This still runs, even though age should be an integer.
# insert_patient_data("Ram", "Rupam")


# ============================================================
# 3. TYPE VALIDATION: Check the actual data types
# ============================================================

def insert_patient_data(name: str, age: int):
    if not isinstance(name, str) or not isinstance(age, int):
        raise TypeError("Name must be a string and age must be an integer.")

    print("Name:", name)
    print("Age:", age)
    print("Data inserted into the database successfully.")


# Correct input
# insert_patient_data("Ram", 25)

# Incorrect input: raises TypeError
# insert_patient_data("Ram", "Rupam")


# ============================================================
# 4. DATA VALIDATION: Check whether values are valid
# ============================================================

def insert_patient_data(name: str, age: int):

    # Step 1: Validate data types
    if not isinstance(name, str) or not isinstance(age, int):
        raise TypeError("Name must be a string and age must be an integer.")

    # Step 2: Validate name
    if not name.strip():
        raise ValueError("Name cannot be empty.")

    # Step 3: Validate age
    if age < 0:
        raise ValueError("Age cannot be negative.")

    # Step 4: Process valid data
    print("Name:", name)
    print("Age:", age)
    print("Data inserted into the database successfully.")


# ============================================================
# 5. TEST THE FUNCTION
# ============================================================

insert_patient_data("Ram", -9)