from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json
app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='id of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description="name of the patient")]
    city: Annotated[str, Field(..., decsription='city of the patient')]
    age: Annotated[int, Field(..., description='age of the patient', gt=0, lt=120)]
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., description='gender of the patient')]
    height: Annotated[float, Field(..., gt=0, decsription='height of the patient')]
    weight: Annotated[float, Field(..., gt=0, description='weight of the patient')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi <18.5:
            return "underweight"
        elif self.bmi <30:
            return "normal"
        else:
            return "obese"

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("patients.json", 'w') as f:
        json.dump(data, f)


@app.get('/')
def hello():
    return {"message": "Welcome to the Patient Health Records API!"}

@app.get('/about')
def about():
    return {'message': 'An API to manage patient health records.'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="patient already exists")
    else:
        data[patient.id] = patient.model_dump(exclude=["id"]) #converts pydantic object to dictionary
        save_data(data)
        return JSONResponse(status_code=201, content={"message": "patient added successfully"})


@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(
    ...,
    description="The ID of the patient to retrieve",
    example="P001"
)):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found.")

@app.get('/sort')
def sort_patients(sort_by: str = Query(
    ...,
    description="The field to sort patients by (e.g., 'age', 'name')",
    example="age"
), order : str = Query(
    'asc', 
    description="The order to sort patients (asc or desc)",
    example="asc"
)):
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are: {', '.join(valid_fields)}")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid sort order. Valid orders are: 'asc' or 'desc'")
    data = load_data()
    sort_order = True if order == 'desc' else False
    sorted_patients = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse = sort_order)
    return sorted_patients