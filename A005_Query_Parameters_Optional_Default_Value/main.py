from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def get_users(name: str = None):
    return {"Name": name}

@app.get("/products")
def get_products(limit: int = 10):
    return {"Limit": limit}

@app.get("items")
def get