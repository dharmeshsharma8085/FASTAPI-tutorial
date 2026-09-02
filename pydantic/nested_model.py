from pydantic import BaseModel

class Address(BaseModel):
    city : str
    state : str
    pincode : int 
    
class patient(BaseModel):
    name : str
    gender : str
    age : int
    address : Address
    
address_dict = { "city":"Delhi" , "state":"Haryana" , "pincode":457547}

address1 = Address(**address_dict)

patient_dict = {
    "name":"Dharmesh",
    "gender":"Male",
    "age":19,
    "address":address1
    }


patient1 = patient(**patient_dict)

print(patient1)