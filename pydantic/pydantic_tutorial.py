from pydantic import BaseModel, EmailStr, Field, StrictBool
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):

    name: Annotated[
        str,
        Field(
            max_length=50,
            title="Patient Name",
            description="Write the name of the patient"
        )
    ]

    age: int = Field(gt=18, lt=60)

    weight: Annotated[
        float,
        Field(gt=0, strict=True)
    ]

    married: Optional[StrictBool] = None

    allergies: Optional[
        Annotated[
            List[str],
            Field(max_length=5)
        ]
    ] = None

    email: EmailStr = Field(max_length=50)

    contact_detail: Dict[str, str]


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
    "age": 20,
    "weight": 78.4,
    "married": True,
    "allergies": ["pollen", "dust"],
    "email": "abc@gmail.com",
    "contact_detail": {
        "phone": "57637573567"
    }
}


patient1 = Patient(**patient_info)

insert_patient_data(patient1)