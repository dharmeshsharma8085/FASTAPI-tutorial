from pydantic import BaseModel, EmailStr , model_validator
from typing import List, Dict, Optional


class Patient(BaseModel):
    name: str
    age: int
    weight: float
    married: Optional[bool] = None
    allergies: Optional[List[str]] = None
    email: EmailStr
    contact_detail: Dict[str, str]
    
    @model_validator(mode="after")
    def validate_emergency_content(cls , model):
        if model.age>60 and "emergency" not in model.contact_detail :
            raise ValueError("Patient older than 60 must have emergency number ")
        return model

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.email)
    print(patient.allergies)
    print(patient.contact_detail)

    print("Inserted")


patient_info = {
    "name": "Dharmesh",
    "age": 90,
    "weight": 78.4,
    "married": True,
    "allergies": ["pollen", "dust"],
    "email": "abc@gmail.com",
    "contact_detail": {
        "phone": "57637573567",
        "emergency": "67888586758"
    }
}


patient1 = Patient(**patient_info)

insert_patient_data(patient1)