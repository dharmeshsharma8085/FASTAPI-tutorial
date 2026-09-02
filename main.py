from fastapi import FastAPI , Path , Query , HTTPException
import json
app= FastAPI()

def load_data():
    with open("patient.json" , "r") as f:
        data = json.load(f)
    return data 


@app.get("/") # route / decorator

def hello():
    return {"message":"Patient management System API"}


@app.get("/about")
def about():
    return { "message" : " A fully functional API to manage your patient records"}

@app.get("/view")
def view():
    data = load_data()
    
    return data 

@app.get("/patient/{patient_id}")
def view_patient(patient_id: int = Path(..., description= "Id of the patient in the Database" , example=101)):
    data = load_data()

    for patient in data:
        if patient["id"] == patient_id:
            return patient
# exception handling
    raise HTTPException(status_code=404 , detail ="Patient Not found")
from fastapi import Query, HTTPException


#(...) required
@app.get("/sort")
def sort_patient(
    sort_by: str = Query(..., description="Sort by height, age, weight"),
    order: str = Query("asc", description="Sort in asc or desc order")
):

    valid_fields = ["height", "weight", "age"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Choose from {valid_fields}"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Choose asc or desc"
        )

    data = load_data()

    reverse_order = True if order == "desc" else False

    sorted_data = sorted(
        data,
        key=lambda x: x.get(sort_by, 0),
        reverse=reverse_order
    )

    return sorted_data