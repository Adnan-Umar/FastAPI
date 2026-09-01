from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def get_users(name: str = None):
    return {"Name": name}

@app.get("/products")
def get_products(limit: int = 10):
    return {"Limit": limit}

# http://127.0.0.1:8000/items?name=mobile&price=20000
@app.get("/items")
def get_items(name: str = None, price: int = 0):
    return {
        "name": name,
        "Price": price
    }