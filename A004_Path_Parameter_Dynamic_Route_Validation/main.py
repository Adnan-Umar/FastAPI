from fastapi import FastAPI

app = FastAPI()

#Users route
@app.get("/users/{user_id}")
def getUserFromId(user_id: int):
    return {"user_id": user_id}