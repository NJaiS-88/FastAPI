from fastapi import FastAPI, Path, HTTPException, Query
import json
app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

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