from fastapi import FastAPI

app = FastAPI()

# Home Page
@app.get("/")
def home():
    return {"message": "Welcome to fastapi"}

# About route
@app.get("/about")
def about():
    return {"message": "This is about page"}

# Users route
@app.get("/users")
def about():
    return {
        "users": ["Adnan", "umar", "Md"]
    }