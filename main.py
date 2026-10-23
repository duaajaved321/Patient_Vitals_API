from fastapi import FastAPI
from datetime import datetime, timezone
from database import create_table, save_vitals, get_patient_vitals, get_patient_summary
from pydantic import BaseModel, Field, StrictInt, StrictStr, field_validator, StrictFloat
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Query

app= FastAPI()
create_table()

@app.get("/health")

def health_check():
    return {"status": "ok",
            "timestamp": datetime.now(timezone.utc).isoformat()}


class BloodPressure(BaseModel):
    systolic: StrictInt = Field(ge=50, le=300)
    diastolic: StrictInt = Field(ge=30, le=200)

class PatientVitals(BaseModel):
    patient_id: StrictStr
    age: StrictInt = Field(ge=0, le=120)
    blood_pressure: BloodPressure
    glucose_level: StrictInt | StrictFloat = Field(gt=0)

    @field_validator("patient_id")
    @classmethod
    def validate_patient_id(cls, value):
        if not value.strip():
            raise ValueError("patient_id cannot be empty")
        return value

@app.post("/vitals")
def add_vitals(vitals: PatientVitals):
    save_vitals(vitals)
    return {"message": "Vitals saved successfully"}

@app.get("/patients/{patient_id}/vitals")
def patient_history(
    patient_id: str,
    limit: int | None = Query(default=None, gt=0)
):
    records = get_patient_vitals(patient_id)
    return records[:limit] if limit is not None else records

@app.get("/patients/{patient_id}/summary")
def patient_summary(patient_id: str):
    summary = get_patient_summary(patient_id)
    return summary

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {
            "field": ".".join(str(part) for part in error["loc"]),
            "message": error["msg"]
        }
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=400,
        content={"detail": errors}
    )
