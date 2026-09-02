from pydantic import BaseModel, EmailStr , field_validator
from typing import List, Dict, Optional


class Patient(BaseModel):
    name: str
    age: int
    weight: float
    married: Optional[bool] = None
    allergies: Optional[List[str]] = None
    email: EmailStr
    contact_detail: Dict[str, str]
    
    
    @field_validator("age" , mode = "after") #before sai yai nhi hoga
    @classmethod
    def validate_age(cls,value):
        if 0<value<100 :
            return value
        else:
            raise ValueError("Please enter valid age and valid datatype")
    @field_validator("email")
    @classmethod
    def emial_validator(cls , value):
        
        valid_domain = [ "hdfc.com" , "icici.com"]
        domain_name = value.split("@")[-1]
        
        if domain_name not in valid_domain:
            raise ValueError("not a valid domain ")
        
        return value
    
    @field_validator("name")
    @classmethod
    def trasform_name(cls, value):
        return value.upper()
    
     
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
    "email": "abc@hdfc.com",
    "contact_detail": {
        "phone": "57637573567"
    }
}


patient1 = Patient(**patient_info) # validation and type  

insert_patient_data(patient1)