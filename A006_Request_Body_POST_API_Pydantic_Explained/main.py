from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

# @app.post("/create-user")
# def create_user(name: str, age: int):
#     return {
#         "Name": name,
#         "Age": age
#     }

# @app.post("/create-user")
# def create_user(user: dict):
#     return {
#         "message": "User created",
#         "data": user
#     }

@app.post("/create-user")
def create_user(user: User):
    return {
        "message": "User created",
        "data": user
    }