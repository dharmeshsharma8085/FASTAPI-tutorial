from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field

from typing import Annotated, Literal, Optional
import json


app = FastAPI(
    title="Patient Management System API",
    description="A FastAPI application to manage patient records",
    version="1.0.0"
)


# =========================================================
# Pydantic Model
# =========================================================

class Patient(BaseModel):

    id: Annotated[
        int,
        Field(
            ...,
            description="Unique ID of the patient",
            examples=[101]
        )
    ]

    name: Annotated[
        str,
        Field(
            ...,
            description="Name of the patient",
            examples=["Rahul Sharma"]
        )
    ]

    city: Annotated[
        str,
        Field(
            ...,
            description="City of the patient",
            examples=["Jaipur"]
        )
    ]

    age: Annotated[
        int,
        Field(
            ...,
            gt=0,
            lt=120,
            description="Age of the patient",
            examples=[24]
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
            description="Height of the patient in feet",
            examples=[5.8]
        )
    ]

    weight: Annotated[
        float,
        Field(
            ...,
            gt=0,
            description="Weight of the patient in kilograms",
            examples=[68.5]
        )
    ]

    # =====================================================
    # Computed Fields
    # =====================================================

    @computed_field
    @property
    def bmi(self) -> float:

        # Feet -> meters
        height_in_meters = self.height * 0.3048

        bmi = round(
            self.weight / (height_in_meters ** 2),
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


# =========================================================
# Patient Update Model
# =========================================================

class PatientUpdate(BaseModel):

    name: Annotated[
        Optional[str],
        Field(default=None)
    ]

    city: Annotated[
        Optional[str],
        Field(default=None)
    ]

    age: Annotated[
        Optional[int],
        Field(
            default=None,
            gt=0,
            lt=120
        )
    ]

    gender: Annotated[
        Optional[Literal["Male", "Female", "Others"]],
        Field(default=None)
    ]

    height: Annotated[
        Optional[float],
        Field(
            default=None,
            gt=0
        )
    ]

    weight: Annotated[
        Optional[float],
        Field(
            default=None,
            gt=0
        )
    ]


# =========================================================
# Load Data
# =========================================================

def load_data():

    with open("patient.json", "r") as f:
        data = json.load(f)

    return data


# =========================================================
# Save Data
# =========================================================

def save_data(data):

    with open("patient.json", "w") as f:
        json.dump(
            data,
            f,
            indent=4
        )


# =========================================================
# Home Route
# =========================================================

@app.get("/")
def hello():

    return {
        "message": "Patient Management System API"
    }


# =========================================================
# About Route
# =========================================================

@app.get("/about")
def about():

    return {
        "message": "A fully functional API to manage your patient records"
    }


# =========================================================
# View All Patients
# =========================================================

@app.get("/view")
def view():

    data = load_data()

    return data


# =========================================================
# View Single Patient
# =========================================================

@app.get("/patient/{patient_id}")
def view_patient(patient_id: int):

    data = load_data()

    for patient in data:

        if patient["id"] == patient_id:

            return patient

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )


# =========================================================
# Sort Patients
# =========================================================

@app.get("/sort")
def sort_patient(

    sort_by: str = Query(
        ...,
        description="Sort by height, weight or age"
    ),

    order: str = Query(
        "asc",
        description="Sort order: asc or desc"
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
        data,
        key=lambda x: x.get(sort_by, 0),
        reverse=reverse_order
    )

    return sorted_data


# =========================================================
# Create Patient
# =========================================================

@app.post("/create")
def create_patient(patient: Patient):

    data = load_data()

    # Check duplicate ID

    for existing_patient in data:

        if existing_patient["id"] == patient.id:

            raise HTTPException(
                status_code=400,
                detail="Patient already exists"
            )

    # Add patient

    data.append(
        patient.model_dump()
    )

    # Save data

    save_data(data)

    return JSONResponse(
        status_code=201,
        content={
            "message": "New record created successfully",
            "patient": patient.model_dump()
        }
    )


# =========================================================
# Update Patient
# =========================================================

@app.put("/edit/{patient_id}")
def update_patient(
    patient_id: int,
    patient_update: PatientUpdate
):

    data = load_data()

    # -----------------------------------------------------
    # Find patient
    # -----------------------------------------------------

    patient_index = None

    for index, patient in enumerate(data):

        if patient["id"] == patient_id:

            patient_index = index
            break

    # -----------------------------------------------------
    # Patient not found
    # -----------------------------------------------------

    if patient_index is None:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # -----------------------------------------------------
    # Existing patient
    # -----------------------------------------------------

    existing_patient_info = data[patient_index]

    # -----------------------------------------------------
    # Get only fields sent by user
    # -----------------------------------------------------

    updated_patient_info = patient_update.model_dump(
        exclude_unset=True
    )

    # -----------------------------------------------------
    # Update patient
    # -----------------------------------------------------

    existing_patient_info.update(
        updated_patient_info
    )

    # Make sure ID remains unchanged

    existing_patient_info["id"] = patient_id

    # -----------------------------------------------------
    # Re-create Pydantic object
    # This validates data and recalculates BMI/verdict
    # -----------------------------------------------------

    patient_pydantic_object = Patient(
        **existing_patient_info
    )

    # -----------------------------------------------------
    # Replace patient in list
    # -----------------------------------------------------

    data[patient_index] = patient_pydantic_object.model_dump()

    # -----------------------------------------------------
    # Save data
    # -----------------------------------------------------

    save_data(data)

    # -----------------------------------------------------
    # Response
    # -----------------------------------------------------

    return JSONResponse(
        status_code=200,
        content={
            "message": "Patient updated successfully",
            "patient": patient_pydantic_object.model_dump()
        }
    )


# =========================================================
# Delete Patient
# =========================================================

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: int):

    data = load_data()

    # -----------------------------------------------------
    # Find patient
    # -----------------------------------------------------

    patient_index = None

    for index, patient in enumerate(data):

        if patient["id"] == patient_id:

            patient_index = index
            break

    # -----------------------------------------------------
    # Patient not found
    # -----------------------------------------------------

    if patient_index is None:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # -----------------------------------------------------
    # Delete patient
    # -----------------------------------------------------

    deleted_patient = data.pop(patient_index)

    # -----------------------------------------------------
    # Save data
    # -----------------------------------------------------

    save_data(data)

    # -----------------------------------------------------
    # Response
    # -----------------------------------------------------

    return JSONResponse(
        status_code=200,
        content={
            "message": "Patient deleted successfully",
            "patient": deleted_patient
        }
    )