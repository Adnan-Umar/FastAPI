# =========================================================
# A019 — UPDATE Operation with Database
# =========================================================
# Walks the full SQLAlchemy READ + UPDATE pattern:
#   - GET  /todos              → list all rows
#   - GET  /todos/{todo_id}    → read a single row (404 if missing)
#   - PUT  /todos/{todo_id}    → update an existing row (404 if missing)
# =========================================================

# --- SQLAlchemy imports: ORM building blocks ---
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# --- FastAPI imports: HTTP framework + dependency injection + errors ---
from fastapi import FastAPI, Depends, HTTPException

# 1. Create the FastAPI app instance (Uvicorn serves THIS object)
app = FastAPI()

# 2. Where the SQLite database file lives (3 slashes = SQLite file path)
DATABASE_URL = "sqlite:///./test.db"

# 3. Create the engine — the connection factory that talks to the DB
#    `check_same_thread=False` lets FastAPI's thread pool share the connection
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 4. Build a session factory — calling `session_local()` produces a new Session
session_local = sessionmaker(bind=engine)

# 5. Declarative base — the parent class that every ORM model inherits from
Base = declarative_base()

# 6. The Todo model — a Python class that maps to the `todos` table
class Todo(Base):
    __tablename__ = "todos"   # SQL table name

    id = Column(Integer, primary_key=True, index=True)   # auto-incrementing PK
    title = Column(String)                                # the todo's text
    completed = Column(String)                            # 'true' / 'false'

# 7. Actually create the table in the DB (idempotent — won't error if it exists)
Base.metadata.create_all(bind=engine)

# 8. Per-request session dependency
#    `yield` makes this a "setup + teardown" dep:
#      - setup:   open a session before the route runs
#      - teardown: close the session after the route (even on errors)
def get_db():
    db = session_local()    # open
    try:
        yield db            # route runs here, `db` is injected
    finally:
        db.close()          # always close


# =========================================================
# CREATE (kept from A017 for context — the tutorial builds on it)
# =========================================================
@app.post("/todos")
def create_todo(title: str, db: Session = Depends(get_db)):
    # Build a Todo instance (id is auto-assigned by the DB on commit)
    todo = Todo(title=title, completed=False)
    db.add(todo)        # stage the INSERT
    db.commit()         # save to the DB
    db.refresh(todo)    # reload — picks up the auto-generated `id`
    return {
        "message": "Todo created",
        "data": todo
    }


# =========================================================
# READ ALL — GET /todos
# =========================================================
# `db.query(Todo)`      → SELECT * FROM todos
# `.all()`              → list of every row as Todo objects
@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    # Run the query: SELECT * FROM todos
    todos = db.query(Todo).all()

    # Return a richer response shape with count + data
    return {
        "message": "",
        "Total": len(todos),   # how many rows came back
        "data": todos
    }


# =========================================================
# READ ONE — GET /todos/{todo_id}
# =========================================================
# `db.query(Todo).filter(Todo.id == todo_id)` → SELECT * FROM todos WHERE id = ?
# `.first()`                                  → first row, or None if no match
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    # SELECT * FROM todos WHERE id = {todo_id} LIMIT 1
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    # If no row matched, raise 404 (proper HTTP error, not 200 + error dict)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Return the matching Todo object
    return todo

# Update
# PUT  /todos/{todo_id}  → update an existing row
# 1. Look up the row by id
# 2. If not found, raise 404
# 3. Mutate the in-memory object's attributes
# 4. `db.commit()` flushes the changes as an UPDATE statement
# 5. `db.refresh()` reloads the row to pick up any DB-side changes
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, title: str, db: Session = Depends(get_db)):
    # SELECT * FROM todos WHERE id = {todo_id} LIMIT 1
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    # If no row matched, raise 404
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Mutate the in-memory object — SQLAlchemy tracks the change
    todo.title = title

    # Commit to send the UPDATE to the DB
    db.commit()

    # Refresh to reload the row (e.g., in case triggers/defaults changed values)
    db.refresh(todo)

    return {
        "message": "Todo updated",
        "data": todo
    }