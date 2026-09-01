from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

todos = []

class Todo(BaseModel):
    id: int
    title: str
    completed: bool

@app.post("/todos")
def create_todo(todo:Todo):
    todos.append(todo)
    return {
        "message":"todo added",
        "data": todo
    }

@app.get("/todos")
def get_todo():
    return {
        "message": "Get Todos",
        "data": todos
    }

@app.get("/todos/{todo_id}")
def get_todo_byId(todo_id:int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return {"error": "todo not found"}

@app.put("/todos/{todo_id}")
def update_todo(todo_id:int, updated_todo:Todo):
    for idx,todo in enumerate(todos):
        if todo.id == todo_id:
            todos[idx] = updated_todo
            return {
                "message":"data updated",
                "data":updated_todo
            }
    return {"error": "TODO not found"}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int):
    for idx,todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(idx)
            return {"message": "Data deleted"}
    return {"message": "data not found"}