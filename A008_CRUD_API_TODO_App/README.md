<div align="center">

# ✅ A008 — CRUD API: TODO App

### *The complete mini-project: 5 endpoints, 1 Pydantic model, 0 lines of boilerplate.*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![CRUD](https://img.shields.io/badge/CRUD-Full-success?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Level-Intermediate-orange?style=for-the-badge)
![Reading Time](https://img.shields.io/badge/Read_Time-45_min-blueviolet?style=for-the-badge)
![Endpoints](https://img.shields.io/badge/Endpoints-5-orange?style=for-the-badge)

</div>

---

## 🧠 The One-Sentence Summary

> **A CRUD app is just a Pydantic model + a Python list + five HTTP verbs; FastAPI's job is to make that combination boringly reliable.**

If you remember *"Pydantic + list + 5 verbs = CRUD"*, the rest of this README is decoration.

---

## 📑 Table of Contents

- [🧠 The One-Sentence Summary](#-the-one-sentence-summary)
- [📖 The Story: A Chalkboard of TODOs](#-the-story-a-chalkboard-of-todos)
- [🎯 What You Will Learn (10 Skills)](#-what-you-will-learn-10-skills)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧬 Anatomy of `main.py` — Line by Line](#-anatomy-of-mainpy--line-by-line)
- [🛣️ API Endpoints (All 5)](#-api-endpoints-all-5)
- [🧠 The Mental Model: CRUD ↔ HTTP Verbs](#-the-mental-model-crud--http-verbs)
- [🧪 Try It With curl (Every Verb)](#-try-it-with-curl-every-verb)
- [🧠 Why `enumerate` + `pop` + `replace`](#-why-enumerate--pop--replace)
- [🧠 Status Codes — What's "Right" vs What This App Does](#-status-codes--whats-right-vs-what-this-app-does)
- [🔧 Suggested Improvements](#-suggested-improvements)
- [⚠️ Common Pitfalls & Fixes](#-common-pitfalls--fixes)
- [🧠 Mnemonic Cheat Sheet](#-mnemonic-cheat-sheet)
- [🧪 Recall Test](#-recall-test)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 📖 The Story: A Chalkboard of TODOs

You run a tiny office ✏️. People add tasks to the chalkboard:

1. ➕ *"Add a task"* — write it on the board
2. 👀 *"Show me the board"* — read everything
3. 🔍 *"Show me task #7"* — read one
4. ✏️ *"Change task #7 to 'finished'"* — replace it
5. 🗑️ *"Erase task #7"* — remove it

That's it. That's the whole app. The chalkboard is a Python list. The "shape" of a task is a Pydantic model. The five verbs are HTTP methods. FastAPI is the invisible hand connecting them.

> 🧠 **Mnemonic:** "**C-R-U-D = P-G-G-P-D**" — **C**reate→**P**OST, **R**ead→**G**ET, **U**pdate→**P**UT, **D**elete→**D**ELETE. The "**G**ET" appears twice because reading is the most common action.

---

## 🎯 What You Will Learn (10 Skills)

| # | 🎯 Skill | 🧠 You'll remember it because... |
|:-:|:---------|:--------------------------------|
| 1 | 🧬 Define a Pydantic `Todo` model | "Class with three fields" |
| 2 | 🟡 `POST` to create | "Add to the list, return the new item" |
| 3 | 🟢 `GET` (list & one) | "Two routes: collection + item" |
| 4 | 🟠 `PUT` to replace | "Find by id, swap in place" |
| 5 | 🔴 `DELETE` to remove | "Find by id, pop it out" |
| 6 | 🔁 `enumerate()` for index + value | "Two cursors at once" |
| 7 | 💥 `pop(idx)` to remove | "Returns AND removes" |
| 8 | 🛡️ Auto-validated request bodies | "Bad JSON never reaches your code" |
| 9 | 📚 Swagger UI for free | "Clickable TODO playground" |
| 10 | 🧠 CRUD ↔ HTTP mapping | "CRUD = POST/GET/PUT/DELETE" |

---

## 📂 Project Structure

```
📁 A008_CRUD_API_TODO_App/
├── 🐍 main.py     ← 52 lines, 5 endpoints, 1 model
└── 📖 README.md   ← you are here
```

> 💡 No `requirements.txt` here — install with `pip install "fastapi[standard]"`.

---

## ⚙️ Installation & Setup

```powershell
cd D:\AllProgram\LEARN\Python\FastAPI\A008_CRUD_API_TODO_App
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "fastapi[standard]"
uvicorn main:app --reload
```

Then open <http://127.0.0.1:8000/docs> — your TODO API is now a clickable website.

---

## 🧬 Anatomy of `main.py` — Line by Line

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

todos = []

class Todo(BaseModel):
    id: int
    title: str
    completed: bool

@app.post("/todos")
def create_todo(todo: Todo):
    todos.append(todo)
    return {
        "message": "todo added",
        "data": todo
    }

@app.get("/todos")
def get_todo():
    return {
        "message": "Get Todos",
        "data": todos
    }

@app.get("/todos/{todo_id}")
def get_todo_byId(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return {"error": "todo not found"}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    for idx, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[idx] = updated_todo
            return {
                "message": "data updated",
                "data": updated_todo
            }
    return {"error": "TODO not found"}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for idx, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(idx)
            return {"message": "Data deleted"}
    return {"message": "data not found"}
```

### Line-by-line

| Lines | Code | 🧠 Why it's there |
|:-----:|:-----|:------------------|
| 1–2 | Imports | FastAPI + Pydantic |
| 4 | `app = FastAPI()` | The single app instance |
| 6 | `todos = []` | The in-memory "chalkboard" |
| 8–11 | `class Todo` | Contract: id (int), title (str), completed (bool) |
| 13–19 | `POST /todos` | **Create** — append + echo |
| 21–26 | `GET /todos` | **Read all** — return list |
| 28–33 | `GET /todos/{id}` | **Read one** — find by id |
| 35–44 | `PUT /todos/{id}` | **Update** — replace in place |
| 46–52 | `DELETE /todos/{id}` | **Delete** — pop by id |

### 🎯 If you remember ONE thing
> **The whole app is one model, one list, and five decorated functions.** Nothing more, nothing less.

---

## 🛣️ API Endpoints (All 5)

Base URL: **`http://127.0.0.1:8000`**

| # | CRUD | Verb | Endpoint | Body | Returns |
|:-:|:----:|:----:|:---------|:----:|:--------|
| 1 | **C**reate | 🟡 POST | `/todos` | `Todo` | `{ message, data: Todo }` |
| 2 | **R**ead all | 🟢 GET | `/todos` | — | `{ message, data: [Todo] }` |
| 3 | **R**ead one | 🟢 GET | `/todos/{todo_id}` | — | `Todo` or `{ error }` |
| 4 | **U**pdate | 🟠 PUT | `/todos/{todo_id}` | `Todo` | `{ message, data }` or `{ error }` |
| 5 | **D**elete | 🔴 DELETE | `/todos/{todo_id}` | — | `{ message }` |

---

### 🟡 1. `POST /todos` — Create a TODO

```bash
curl -X POST http://127.0.0.1:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"id":1,"title":"Learn FastAPI","completed":false}'
```

```json
{
  "message": "todo added",
  "data": {
    "id": 1,
    "title": "Learn FastAPI",
    "completed": false
  }
}
```

**What happens under the hood:**

```
1. Uvicorn receives POST /todos
2. FastAPI parses JSON body
3. Pydantic validates against Todo schema
4. ✅ Valid → calls create_todo(todo)
5. Function appends to todos list
6. Returns the Todo → serialized to JSON
```

---

### 🟢 2. `GET /todos` — List all TODOs

```bash
curl http://127.0.0.1:8000/todos
```

```json
{
  "message": "Get Todos",
  "data": [
    {"id": 1, "title": "Learn FastAPI", "completed": false},
    {"id": 2, "title": "Write README", "completed": true}
  ]
}
```

---

### 🟢 3. `GET /todos/{todo_id}` — Read one TODO

```bash
curl http://127.0.0.1:8000/todos/1
```

```json
{"id": 1, "title": "Learn FastAPI", "completed": false}
```

If the id doesn't exist:

```json
{"error": "todo not found"}
```

**Note:** the error response has status `200 OK` (this app doesn't use `404`). See the *Status Codes* section below.

---

### 🟠 4. `PUT /todos/{todo_id}` — Update a TODO

```bash
curl -X PUT http://127.0.0.1:8000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"id":1,"title":"Learn FastAPI deeply","completed":true}'
```

```json
{
  "message": "data updated",
  "data": {
    "id": 1,
    "title": "Learn FastAPI deeply",
    "completed": true
  }
}
```

If not found:

```json
{"error": "TODO not found"}
```

> 💡 **Why `PUT` and not `PATCH`?** `PUT` *replaces* the entire resource. `PATCH` would only update the fields you send. The current code expects a full `Todo` body — that's classic `PUT` semantics.

---

### 🔴 5. `DELETE /todos/{todo_id}` — Delete a TODO

```bash
curl -X DELETE http://127.0.0.1:8000/todos/1
```

```json
{"message": "Data deleted"}
```

If not found:

```json
{"message": "data not found"}
```

---

## 🧠 The Mental Model: CRUD ↔ HTTP Verbs

| CRUD | HTTP Verb | SQL analog | What it does to the list |
|:----:|:---------:|:-----------|:-------------------------|
| **C**reate | 🟡 POST | `INSERT` | `todos.append(item)` |
| **R**ead | 🟢 GET | `SELECT` | `return todos` (or filter by id) |
| **U**pdate | 🟠 PUT | `UPDATE` | `todos[idx] = new_item` |
| **D**elete | 🔴 DELETE | `DELETE` | `todos.pop(idx)` |

> 🧠 **Mnemonic:** "**CRUD → PGP-D**" → **P**OST, **G**ET, **P**UT, **D**ELETE. Sounded out: *"Cuddle PGP-D."*

### Visualizing the List as a Chalkboard

```
BEFORE:
┌────┬──────────────────────┬───────────┐
│ id │ title                │ completed │
├────┼──────────────────────┼───────────┤
│  1 │ Learn FastAPI        │   false   │
│  2 │ Write README         │   true    │
└────┴──────────────────────┴───────────┘

DELETE /todos/1  →  todos.pop(0)

AFTER:
┌────┬──────────────────────┬───────────┐
│ id │ title                │ completed │
├────┼──────────────────────┼───────────┤
│  2 │ Write README         │   true    │
└────┴──────────────────────┴───────────┘
```

---

## 🧪 Try It With curl (Every Verb)

```bash
# 1. Create
curl -X POST http://127.0.0.1:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"id":1,"title":"Learn FastAPI","completed":false}'

curl -X POST http://127.0.0.1:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"id":2,"title":"Write README","completed":false}'

# 2. Read all
curl http://127.0.0.1:8000/todos

# 3. Read one
curl http://127.0.0.1:8000/todos/1

# 4. Update
curl -X PUT http://127.0.0.1:8000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"id":1,"title":"Master FastAPI","completed":true}'

# 5. Delete
curl -X DELETE http://127.0.0.1:8000/todos/2
```

### ❌ Try a 422 (bad body) to see validation in action

```bash
curl -X POST http://127.0.0.1:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"id":"not-an-int","title":"oops","completed":"yes"}'
```

→ Returns `422 Unprocessable Entity` with field-level error. Your function never runs.

---

## 🧠 Why `enumerate` + `pop` + `replace`

### `enumerate` — index AND value

```python
for idx, todo in enumerate(todos):
    ...
```

Without `enumerate` you'd write:
```python
for i in range(len(todos)):
    if todos[i].id == todo_id:
        ...
```

`enumerate` is the **Pythonic** way. It hands you both the index (`idx`) and the value (`todo`) on each iteration.

> 🧠 **Mnemonic:** "**E**numerate = **E**lement + position."

### `pop(idx)` — remove AND return

```python
todos.pop(idx)
```

- `list.pop()` — removes the **last** item
- `list.pop(i)` — removes the item at index `i` and **returns it**

This is why `DELETE` can return the deleted object:

```python
deleted = todos.pop(idx)
return deleted
```

### `todos[idx] = new_item` — replace in place

```python
todos[idx] = updated_todo
```

This overwrites the slot. The list keeps the same length, just a different value at that index.

> 🧠 **Mnemonic:** "**Pop = remove, Index = replace**."

---

## 🧠 Status Codes — What's "Right" vs What This App Does

| Endpoint | App returns | "Correct" | Why the difference |
|:---------|:-----------:|:---------:|:-------------------|
| `POST /todos` | `200` | `201 Created` | Convention: POST should signal "something was created" |
| `GET /todos` | `200` | `200` | ✅ Correct |
| `GET /todos/999` | `200 + {error}` | `404 Not Found` | The app returns errors inside the body, not via status code |
| `PUT /todos/999` | `200 + {error}` | `404 Not Found` | Same as above |
| `DELETE /todos/999` | `200 + {error}` | `404 Not Found` | Same as above |

This is fine for a learning project. For production, use `HTTPException`:

```python
from fastapi import HTTPException, status

@app.get("/todos/{todo_id}")
def get_todo_byId(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="todo not found"
    )
```

> 🧠 **Mnemonic:** "**Right code = right semantic**." Browsers and clients *do* use status codes, not just bodies.

---

## 🔧 Suggested Improvements

### 1️⃣ Return `201 Created` on POST

```python
from fastapi import status

@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(todo: Todo):
    todos.append(todo)
    return {"message": "todo added", "data": todo}
```

### 2️⃣ Use `HTTPException` for errors

```python
from fastapi import HTTPException

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for idx, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(idx)
            return {"message": "Data deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")
```

### 3️⃣ Reject duplicate IDs

```python
@app.post("/todos", status_code=201)
def create_todo(todo: Todo):
    if any(t.id == todo.id for t in todos):
        raise HTTPException(status_code=409, detail="ID already exists")
    todos.append(todo)
    return todo
```

### 4️⃣ Use `PATCH` for partial updates

```python
from pydantic import BaseModel

class TodoUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

@app.patch("/todos/{todo_id}")
def patch_todo(todo_id: int, changes: TodoUpdate):
    for idx, todo in enumerate(todos):
        if todo.id == todo_id:
            update = todo.model_dump()
            if changes.title is not None:
                update["title"] = changes.title
            if changes.completed is not None:
                update["completed"] = changes.completed
            todos[idx] = Todo(**update)
            return todos[idx]
    raise HTTPException(status_code=404, detail="Todo not found")
```

### 5️⃣ Use `response_model` for safety

```python
@app.get("/todos", response_model=list[Todo])
def get_todo():
    return todos
```

Now FastAPI:
- ✅ Validates the response
- ✅ Filters out any extra fields
- ✅ Documents the schema in `/docs`

---

## ⚠️ Common Pitfalls & Fixes

| 😖 Pitfall | 🔍 Cause | ✅ Fix |
|:-----------|:---------|:------|
| `POST` returns 200 not 201 | Default status | Add `status_code=201` to decorator |
| Errors return 200 | Returning dict instead of raising | Use `HTTPException(404, ...)` |
| Duplicate IDs accepted | No check in `create_todo` | Check before append |
| Can't `PUT` partially | `PUT` replaces the whole object | Use `PATCH` for partial |
| List wipes on restart | In-memory storage | Add a database (later module) |
| `todos.pop(idx)` crashes | `idx` out of range | Impossible here (we found it in the loop) |

---

## 🧠 Mnemonic Cheat Sheet

| Concept | Mnemonic | Story |
|:--------|:---------|:------|
| CRUD ↔ HTTP | **PGP-D** | POST, GET, PUT, DELETE — *"Cuddle PGP-D"* |
| The 5 endpoints | **C-R-R-U-D** | Create, Read-all, Read-one, Update, Delete |
| `enumerate` | **Element + position** | Two cursors at once |
| `pop` vs `[]=` | **Pop = remove, Index = replace** | Two list operations |
| Status codes | **Right code = right semantic** | Browsers read them |
| Storage | **Chalkboard** | Visible, fast, vanishes on close |

---

## 🧪 Recall Test

1. What HTTP verb maps to "Update"?
2. What's the difference between `todos.pop()` and `todos.pop(i)`?
3. Why use `enumerate` instead of `range(len(todos))`?
4. What status code *should* `POST` return, and what does this app return?
5. How do you return a proper `404` instead of an error dict?
6. What's the difference between `PUT` and `PATCH`?
7. Why is `response_model` useful?

> 7/7 → you're ready to build a real TODO API with a database.

---

## 🚀 Where to Go Next

| Direction | Module |
|:----------|:-------|
| ⬅️ Previous | [A007](../A007_Pydanti_Models_Data_Validation_Nested_Schemas/) — Nested schemas |
| ⬅️ Back | [Root README](../README.md) |
| ➡️ Next | A009 (planned) — SQLAlchemy database integration |
| ➡️ Future | A010 (planned) — Authentication with OAuth2 + JWT |

---

<div align="center">

### ✅ *You built a complete CRUD API in 52 lines.* ✅

Made with ❤️ and a chalkboard that survives server restarts (in production, with a database).

---

## 🎯 Interview Q&A

### Q1: How do you map CRUD operations to HTTP verbs?

**Answer:**

| CRUD | Verb | Endpoint pattern |
|:-----|:-----|:-----------------|
| **C**reate | `POST` | `/resource` (with body) |
| **R**ead (all) | `GET` | `/resource` |
| **R**ead (one) | `GET` | `/resource/{id}` |
| **U**pdate | `PUT` | `/resource/{id}` (with body) |
| **D**elete | `DELETE` | `/resource/{id}` |

> **One-liner:** *"CRUD ↔ POST/GET/PUT/DELETE."*

### Q2: How would you add pagination to the GET endpoint?

**Answer:** Use **query parameters**:

```python
@app.get("/todos")
def get_todos(skip: int = 0, limit: int = 10):
    return todos[skip : skip + limit]
```

```bash
GET /todos?skip=20&limit=10
```

> **One-liner:** *"`?skip=N&limit=M` paginates a list."*

### Q3: How do you handle "Todo not found" properly?

**Answer:** Raise `HTTPException` instead of returning a dict:

```python
from fastapi import HTTPException

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")
```

This returns proper status `404`, not `200 + {error: ...}`.

> **One-liner:** *"Raise `HTTPException(404, ...)` for missing resources."*

### Q4: Why does `POST` return 201 and not 200 in production?

**Answer:** Convention. `201 Created` semantically signals that a new resource was created. Browsers, CDNs, and clients use the status code to react.

```python
from fastapi import status

@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(todo: Todo): ...
```

> **One-liner:** *"POST creates → 201 Created."*

### Q5: What's the difference between `PUT` and `PATCH`?

**Answer:**

| `PUT` | `PATCH` |
|:------|:--------|
| Replaces the whole resource | Updates only the fields you send |
| Body must contain all fields | Body contains only changed fields |
| Idempotent | Idempotent in semantics, but depends on impl |

```python
# PUT
@app.put("/todos/{todo_id}")
def update(todo_id: int, todo: Todo): ...    # full replacement

# PATCH
@app.patch("/todos/{todo_id}")
def patch(todo_id: int, changes: TodoUpdate): ...   # partial
```

> **One-liner:** *"PUT replaces; PATCH edits."*

### Q6: How do you make the in-memory list thread-safe?

**Answer:** Use a `threading.Lock` or replace the list with a proper DB:

```python
import threading
lock = threading.Lock()

@app.post("/todos")
def create_todo(todo: Todo):
    with lock:
        todos.append(todo)
    return todo
```

For real concurrency, use a database (Postgres, SQLite with WAL mode).

> **One-liner:** *"Use a `Lock` for in-memory, or move to a DB."*

### Q7: How do you prevent duplicate IDs?

**Answer:** Check before appending:

```python
@app.post("/todos", status_code=201)
def create_todo(todo: Todo):
    if any(t.id == todo.id for t in todos):
        raise HTTPException(409, "ID already exists")
    todos.append(todo)
    return todo
```

`409 Conflict` is the correct status for duplicate keys.

> **One-liner:** *"Check first, raise 409 Conflict on duplicate."*

### Q8: What's `response_model` and why use it on GET?

**Answer:** `response_model=Todo` tells FastAPI:
- Validate the response matches `Todo`
- Filter out extra fields
- Document the response schema in `/docs`

```python
@app.get("/todos", response_model=list[Todo])
def get_todos(): return todos
```

> **One-liner:** *"`response_model` = input filter + output guard."*

</div>