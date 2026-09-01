from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#Create Schema | Data validation
# class User(BaseModel):
#     name: str
#     age: int
#     email: str

# @app.post("/create_user")
# def create_user(user: User):
#     return {
#         "message":"User Created",
#         "data": user
#     }

class Address(BaseModel):
    city:str
    pincode:int

# Nested Schema
class User(BaseModel):
    name:str
    age:int
    address: Address

@app.post("/create_user")
def create_user(user:User):
    return{
        "message":"User Created",
        "data":user
    }