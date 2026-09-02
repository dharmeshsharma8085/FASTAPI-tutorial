from pydantic import BaseModel, EmailStr , computed_field
from typing import List, Dict, Optional


class Patient(BaseModel):
    name: str
    age: int
    height:float
    weight: float
    married: Optional[bool] = None
    allergies: Optional[List[str]] = None
    email: EmailStr
    contact_detail: Dict[str, str]
    
    @computed_field
    @property
    def cal_bmi(self) -> float:
        bmi = round((self.weight)/ ((self.height/100)**2) , 2)
        return bmi

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.height)
    print(patient.married)
    print(patient.email)
    print(patient.allergies)
    print(patient.contact_detail)
    print("BMI" , patient.cal_bmi)

    print("Inserted")


patient_info = {
    "name": "Dharmesh",
    "age": 20,
    "height":192.9,
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