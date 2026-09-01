from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age:int
    password:str

# Response Model
class UserResponse(BaseModel):
    name:str
    age:int

@app.get("/user", response_model=UserResponse)
def get_user():
    return{
        "name":"Adnan",
        "age":21,
        "password":"123456"
    }