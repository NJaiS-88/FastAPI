from fastapi import FastAPI
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
