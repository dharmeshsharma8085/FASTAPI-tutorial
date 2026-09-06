from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field

from typing import Annotated, Literal
import json


app = FastAPI()


# =========================
# Pydantic Model
# =========================

class Patient(BaseModel):

    id: Annotated[
        int,
        Field(
            ...,
            description="ID of the patient",
            examples=[100]
        )
    ]

    name: Annotated[
        str,
        Field(
            ...,
            description="Name of the patient",
            examples=["Rakesh"]
        )
    ]

    city: Annotated[
        str,
        Field(
            ...,
            description="City of the patient",
            examples=["Mumbai"]
        )
    ]

    age: Annotated[
        int,
        Field(
            ...,
            gt=0,
            lt=120,
            description="Age of the patient",
            examples=[19]
        )
    ]

    gender: Annotated[
        Literal["Male", "Female", "Others"],
        Field(
            ...,
            description="Gender of the patient",
            examples=["Male"]
        )
    ]

    height: Annotated[
        float,
        Field(
            ...,
            gt=0,
            description="Height of the patient in centimeters"
        )
    ]

    weight: Annotated[
        float,
        Field(
            ...,
            gt=0,
            description="Weight of the patient in kilograms"
        )
    ]


    # =========================
    # Computed Fields
    # =========================

    @computed_field
    @property
    def bmi(self) -> float:

        bmi = round(
            self.weight / ((self.height / 100) ** 2),
            2
        )

        return bmi


    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return "Underweight"

        elif self.bmi < 25:
            return "Normal"

        else:
            return "Overweight"


# =========================
# Load Data
# =========================

def load_data():

    with open("patient.json", "r") as f:
        data = json.load(f)

    return data


# =========================
# Save Data
# =========================

def save_data(data):

    with open("patient.json", "w") as f:
        json.dump(data, f, indent=4)


# =========================
# Home Route
# =========================

@app.get("/")
def hello():

    return {
        "message": "Patient Management System API"
    }


# =========================
# About Route
# =========================

@app.get("/about")
def about():

    return {
        "message": "A fully functional API to manage your patient records"
    }


# =========================
# View All Patients
# =========================

@app.get("/view")
def view():

    data = load_data()

    return data


# =========================
# View Single Patient
# =========================

@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: int = Path(
        ...,
        description="ID of the patient in the database",
        examples=[101]
    )
):

    data = load_data()

    patient_id = str(patient_id)

    if patient_id in data:

        return data[patient_id]

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )


# =========================
# Sort Patients
# =========================

@app.get("/sort")
def sort_patient(

    sort_by: str = Query(
        ...,
        description="Sort by height, age, weight"
    ),

    order: str = Query(
        "asc",
        description="Sort in asc or desc order"
    )
):

    valid_fields = [
        "height",
        "weight",
        "age"
    ]

    # Validate sort field

    if sort_by not in valid_fields:

        raise HTTPException(
            status_code=400,
            detail=f"Choose from {valid_fields}"
        )


    # Validate order

    if order not in ["asc", "desc"]:

        raise HTTPException(
            status_code=400,
            detail="Choose asc or desc"
        )


    data = load_data()


    reverse_order = order == "desc"


    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=reverse_order
    )


    return sorted_data


# =========================
# Create Patient
# =========================

@app.post("/create")
def create_patient(patient: Patient):

    data = load_data()


    # Check if patient already exists

    if str(patient.id) in data:

        raise HTTPException(
            status_code=400,
            detail="Patient already exists"
        )


    # Add new patient

    data[str(patient.id)] = patient.model_dump(
        exclude=["id"]
    )


    # Save data

    save_data(data)


    return JSONResponse(
        status_code=201,
        content={
            "message": "New record created successfully"
        }
    )