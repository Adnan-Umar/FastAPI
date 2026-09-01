from fastapi import FastAPI, Depends, Header, HTTPException

app = FastAPI()

def verify_token(token:str = Header(None)):
    if token != "mysecrettoken":
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    return {
        "user":"Authorized user"
    }

@app.get("/secure-data")
def secure_data(user = Depends(verify_token)):
    return{
        "message":"Secured data accessed",
        "user":user
    }

# def common_logic():
#     return{
#         "message":"Common Logic Executed"
#     }

# # Dependency Injection
# @app.get("/home")
# def home(data = Depends(common_logic)):
#     return data

# Reusable logic
# def get_current_user():
#     return{
#         "user":"Adnan"
#     }

# # Reuse get current user
# @app.get("/profile")
# def get_profile(user = Depends(get_current_user)):
#     return user

# @app.get("/dashboard")
# def dashboard(user = Depends(get_current_user)):
    # return user

