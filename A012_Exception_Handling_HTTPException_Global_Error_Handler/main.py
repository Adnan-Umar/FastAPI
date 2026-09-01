from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Custom Exception
class UserNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name

# Global Exception | error Handler
@app.exception_handler(UserNotFoundException)
def user_not_found_handler(request:Request, exe:UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "status":"error",
            "message":f"User {exe.name} not found"
        }
    )

@app.get("/user/{name}")
def get_user(name:str):
    if name != "Adnan":
        raise UserNotFoundException(
            name
        )
    return {
        "name":name
    }

# Http Exception
# @app.get("/users/{user_id}")
# def get_user(user_id:int):
#     if user_id != 1:
#         raise HTTPException(
#             status_code=404,
#             detail="User Not Found"
#         )
    
#     return{
#         "id":1,
#         "name":"Adnan"
#     }

