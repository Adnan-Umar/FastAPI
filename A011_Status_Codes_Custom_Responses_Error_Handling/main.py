from fastapi import FastAPI, status, HTTPException

app = FastAPI()

# HTTP Status Code
@app.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user():
    return{
        "message":"user created"
    }

# Custom error response
@app.get("/user")
def get_users():
    return {
        "status":"Success",
        "message":"User Fetched",
        "data":{
            "name":"Adnan",
            "age":21
        }
    }

# Error Handling Basic
@app.get("/users/{user_id}")
def get_user(user_id:int):
    if user_id != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not found"
        )

    return {
        "id":1,
        "name":"Adnan"
    }