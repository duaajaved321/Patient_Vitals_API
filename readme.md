# Patient Vitals REST API


A RESTful API built using **FastAPI, Pydantic, and SQLite** to collect, validate, store, retrieve, and summarize patient health metrics.

The project demonstrates backend API development, structured input validation, persistent database storage, error handling, and automated endpoint testing.

## 1. Project Overview

The objective of this project is to develop a lightweight backend service for managing patient vitals through REST API endpoints.

The application accepts patient health measurements, validates incoming data against predefined constraints, stores valid records in SQLite, and provides historical records and aggregated summaries for individual patients.

**Core functionalities:**
- Receive patient vitals through HTTP POST requests.
- Validate required fields, data types, and numerical ranges.
- Persist patient records using SQLite.
- Retrieve historical vitals for individual patients.
- Support optional limits on retrieved records.
- Calculate average blood pressure, average glucose levels, and total record counts.
- Return structured JSON responses and descriptive validation errors.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Backend programming |
| FastAPI | REST API development |
| Pydantic | Input validation and data modeling |
| SQLite | Persistent database storage |
| Uvicorn | ASGI application server |
| pytest | Automated testing |
| HTTPX / TestClient | API endpoint testing |
| Swagger UI | Interactive API documentation |

## 3. Project Structure

```text
patients_vitals_api/
├── main.py
├── database.py
├── test_api.py
├── requirements.txt
├── .gitignore
└── README.md
```

- **main.py:** API routes, Pydantic models, validation, and exception handling.
- **database.py:** SQLite connection, table creation, insertion, retrieval, and aggregation.
- **test_api.py:** Automated endpoint and validation tests.
- **requirements.txt:** Python dependencies.

The SQLite database file is created automatically when the application initializes.

## 4. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Returns service status and current UTC timestamp |
| POST | `/vitals` | Validates and stores patient vitals |
| GET | `/patients/{patient_id}/vitals` | Retrieves historical vitals, with optional `limit` |
| GET | `/patients/{patient_id}/summary` | Returns average metrics and record count |

### Example: Submit Patient Vitals

**Endpoint:** `POST /vitals`

Request body:

```json
{
  "patient_id": "P001",
  "age": 25,
  "blood_pressure": {
    "systolic": 120,
    "diastolic": 80
  },
  "glucose_level": 95
}
```

Successful response:

```json
{
  "message": "Vitals saved successfully"
}
```

### Example: Retrieve Patient Summary

**Endpoint:** `GET /patients/P001/summary`

Example response, assuming two records exist:

```json
{
  "avg_systolic": 125.0,
  "avg_diastolic": 85.0,
  "avg_glucose": 100.0,
  "total_records": 2
}
```

## 5. Input Validation

Pydantic is used to enforce the following rules:

| Field | Validation |
|---|---|
| patient_id | Required, non-empty string |
| age | Integer between 0 and 120 |
| systolic | Integer between 50 and 300 |
| diastolic | Integer between 30 and 200 |
| glucose_level | Positive integer or floating-point number |

Invalid submissions return **HTTP 400 Bad Request** with descriptive error messages through a custom FastAPI exception handler.

## 6. Installation and Setup

**Prerequisites:** Python 3.11 and Conda or an equivalent Python environment.

**Step 1: Clone the repository**

```bash
git clone <repository-url>
cd patients_vitals_api
```

**Step 2: Create and activate an environment**

```bash
conda create -n patient_vitals_api python=3.11 -y
conda activate patient_vitals_api
```

**Step 3: Install dependencies**

```bash
python -m pip install -r requirements.txt
```

**Step 4: Start the application**

```bash
uvicorn main:app --reload
```

**Step 5: Open the API documentation**

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows users to explore and execute the API endpoints directly.

## 7. Automated Testing

Automated tests are implemented using pytest and FastAPI's TestClient.

Test coverage includes:
- Health-check responses
- Successful vitals submissions
- Patient history retrieval
- Optional record limits
- Patient summary calculations
- Missing and empty patient identifiers
- Invalid data types
- Out-of-range measurements
- HTTP 400 validation responses

Run the test suite:

```bash
python -m pytest -v
```

Tests use a temporary SQLite database to avoid modifying existing application records.

## 8. Implementation Highlights

- Separated API route logic from database operations.
- Used nested Pydantic models to represent blood pressure measurements.
- Implemented custom request-validation error handling.
- Used parameterized SQL queries for safe database operations.
- Implemented persistent storage with SQLite.
- Added reusable database functions for inserts, historical retrieval, and aggregation.
- Used automated tests to verify API behavior.

## 9. Limitations

- Designed for local development and academic demonstration.
- Does not include authentication or authorization.
- Does not provide production-grade patient data security.
- Uses SQLite rather than a centralized database server.
- Uses fictional patient data for testing and demonstration.

**Privacy note:** This project is intended for learning purposes and should not be deployed with real identifiable patient health information without appropriate security, privacy, and compliance safeguards.

## 10. Learning Outcomes

Through this project, I gained practical experience in:

- Building RESTful APIs with FastAPI.
- Understanding HTTP methods, request bodies, and path/query parameters.
- Designing nested data models with Pydantic.
- Applying data validation and custom exception handling.
- Integrating SQLite with Python backend services.
- Separating database operations from API route logic.
- Writing automated tests for backend applications.
- Structuring and documenting a reproducible Python project.

---

**Project