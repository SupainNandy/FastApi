# FastAPI and Machine Learning Projects

A hands-on Python learning repository focused on FastAPI, REST API development, data validation, and Machine Learning integration. This repository documents my learning journey through practical examples, from building basic APIs to integrating trained Machine Learning models with backend services and interactive frontends.

## Featured Project: Insurance Premium Prediction

An end-to-end Machine Learning application that predicts an estimated insurance premium based on user-provided information. The project combines a FastAPI backend with a Streamlit frontend to demonstrate how a trained Machine Learning model can be integrated into a web application.

### Features

- **FastAPI Backend:** Provides REST API endpoints for Machine Learning predictions.
- **Machine Learning Integration:** Uses a trained model to estimate insurance premiums.
- **Streamlit Frontend:** Provides an interactive interface for entering user details and viewing predictions.
- **Input Validation:** Handles structured input data using Python type hints and Pydantic.
- **API Communication:** Sends prediction requests from the Streamlit frontend to the FastAPI backend.
- **Error Handling:** Handles API connection failures and unsuccessful responses.
- **Interactive API Documentation:** Supports Swagger UI and ReDoc through FastAPI.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | REST API development |
| Uvicorn | ASGI server |
| Scikit-learn | Machine Learning model integration |
| Pandas | Data processing and manipulation |
| Pydantic | Data validation |
| Streamlit | Interactive frontend |
| Requests | HTTP communication |

## Project Structure

```text
fastApi/
├── 1_Lecture/
├── 2_lecture/
├── 3_lecture/
├── 4_lecture/
├── 5_lecture/
│   ├── frontend.py
│   └── requirements.txt
└── README.md
```

The lecture directories contain practical examples and exercises covering different FastAPI concepts. The fifth lecture includes the Streamlit frontend for the Insurance Premium Prediction application.

## Getting Started

### Prerequisites

Ensure that the following tools are installed on your system:

- Python
- Git
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/SupainNandy/fastApi.git
cd fastApi
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
venv\Scripts\activate
```

On macOS or Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

Navigate to the project directory containing the frontend requirements:

```bash
cd 5_lecture
pip install -r requirements.txt
```

Use the Python version and dependency versions compatible with your trained model and project requirements.

### 4. Start the FastAPI Backend

Run the FastAPI application from the directory containing your backend entry-point file.

For example, if the application is defined in `main.py`:

```bash
uvicorn main:app --reload
```

The backend will typically be available at:

- API URL: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

Replace `main:app` with your actual module and application variable if they differ.

### 5. Start the Streamlit Frontend

Open a second terminal and activate the virtual environment.

Navigate to the directory containing `frontend.py`:

```bash
cd 5_lecture
streamlit run frontend.py
```

Streamlit will provide a local URL, usually:

http://localhost:8501

Ensure that the FastAPI backend is running before making predictions through the frontend.

## Application Workflow

The application follows this workflow:

1. The user enters the required information through the Streamlit interface.
2. The frontend prepares the input data as a JSON payload.
3. The frontend sends an HTTP POST request to the FastAPI `/predict` endpoint.
4. FastAPI validates the incoming request.
5. The trained Machine Learning model generates a premium prediction.
6. FastAPI returns the prediction in JSON format.
7. Streamlit displays the result to the user.

```text
User Input
    |
    v
Streamlit Frontend
    |
    | HTTP POST Request
    v
FastAPI Backend
    |
    v
Input Validation
    |
    v
Trained ML Model
    |
    v
Prediction Response
    |
    v
Streamlit Result Display
```

## API Testing

FastAPI automatically generates interactive API documentation.

To test the prediction endpoint:

1. Start the FastAPI backend.
2. Open http://127.0.0.1:8000/docs.
3. Locate the `POST /predict` endpoint.
4. Click **Try it out**.
5. Provide valid input data in the request body.
6. Execute the request and inspect the JSON response.

The response structure depends on the backend implementation. Use the actual response schema defined by your API.

## Learning Objectives

This repository focuses on developing practical skills in:

- Building REST APIs using FastAPI.
- Understanding HTTP methods, endpoints, and status codes.
- Validating request data with Pydantic.
- Processing structured data with Python and Pandas.
- Integrating trained Machine Learning models into backend services.
- Connecting frontend applications with backend APIs.
- Building interactive Machine Learning applications using Streamlit.
- Handling exceptions and debugging API communication.
- Organising Python projects and managing dependencies.

## Future Improvements

- Add automated tests for API endpoints.
- Improve request and response validation.
- Add Machine Learning model evaluation metrics.
- Improve prediction result visualisation.
- Containerise the application using Docker.
- Deploy the backend and frontend to cloud platforms.
- Implement structured logging and improved error handling.

## About Me

I am a software developer learning Python backend development and Machine Learning integration through practical projects. This repository represents my ongoing journey toward building reliable APIs and integrating Machine Learning models into real-world applications.

**GitHub:** [SupainNandy](https://github.com/SupainNandy)

## Disclaimer

This project is developed for educational purposes. Insurance premium predictions are estimates generated by a Machine Learning model and should not be considered official insurance quotes or financial advice.
