from fastapi import FastAPI
from pydantic import BaseModel
from TaskManager_BrenoJuan.testecalculator.calculator import calculate

# uvicorn TaskManager_BrenoJuan.projetobreno.fast_api:app --reload
# http://127.0.0.1:8000/docs#/

class User_input(BaseModel):
    operation : str
    x : float
    y : float

app = FastAPI()

@app.post("/calculate")
def operate(input:User_input):
    result = calculate(input.operation, input.x, input.y)
    return result