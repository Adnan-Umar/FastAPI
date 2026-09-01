<div align="center">

# 🏛️ A016 — SQLAlchemy Setup: Models, Engine & Database Integration

### *Stop writing SQL. Define tables as Python classes.*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![ORM](https://img.shields.io/badge/ORM-✅-blueviolet?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Level-Advanced-red?style=for-the-badge)
![Reading Time](https://img.shields.io/badge/Read_Time-60_min-blueviolet?style=for-the-badge)
![Lines of Code](https://img.shields.io/badge/Lines_of_Code-39-informational?style=for-the-badge)

</div>

---

## 🧠 The One-Sentence Summary

> **SQLAlchemy lets you define database tables as Python classes (`Base` + `Column` + `__tablename__`), and an ORM `Session` translates your object manipulations into SQL — so you never write a `CREATE TABLE` again.**

If you remember *"Base + Column + Session = tables as objects"*, the rest of this README is decoration.

---

## 📑 Table of Contents

- [🧠 The One-Sentence Summary](#-the-one-sentence-summary)
- [📖 The Story: The Translator](#-the-story-the-translator)
- [🎯 What You Will Learn (15 Skills — heavy module)](#-what-you-will-learn-15-skills--heavy-module)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧬 Anatomy of `main.py` — Line by Line](#-anatomy-of-mainpy--line-by-line)
- [🛣️ API Endpoints](#-api-endpoints)
- [🧠 The Mental Model: 5 Layers of SQLAlchemy](#-the-mental-model-5-layers-of-sqlalchemy)
- [🆕 Every New Keyword & Function Explained](#-every-new-keyword--function-explained)
- [🆚 Raw `sqlite3` (A015) vs SQLAlchemy (A016)](#-raw-sqlite3-a015-vs-sqlalchemy-a016)
- [🔧 Variations: Add Full CRUD with SQLAlchemy](#-variations-add-full-crud-with-sqlalchemy)
- [🧪 Try It With curl + Python REPL](#-try-it-with-curl--python-repl)
- [⚠️ Common Pitfalls & Fixes](#-common-pitfalls--fixes)
- [🧠 Mnemonic Cheat Sheet](#-mnemonic-cheat-sheet)
- [🧪 Recall Test](#-recall-test)
- [🎯 Interview Q&A](#-interview-qa)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 📖 The Story: The Translator

In A015, you spoke directly to the database. You wrote SQL like `INSERT INTO todos VALUES (...)` and Python sent it. **You** were the translator.

In A016, you hire a translator 🏛️ — **SQLAlchemy** — and speak your native language: **Python objects**.

| Without ORM (A015) | With ORM (A016) |
|:-------------------|:-----------------|
| You write SQL | You write Python classes |
| `cursor.execute("INSERT ...")` | `db.add(todo); db.commit()` |
| Raw rows as tuples | Real Python objects |
| Dialect-specific SQL | SQLAlchemy writes the right SQL |
| Manual mapping | Automatic mapping |

> 🧠 **Mnemonic:** "**SQLAlchemy = translator. Speak Python, get SQL.**"

---

## 🎯 What You Will Learn (15 Skills — heavy module)

| # | 🎯 Skill | 🧠 You'll remember it because... |
|:-:|:---------|:--------------------------------|
| 1 | 🏛️ **What SQLAlchemy is** | "ORM = Object-Relational Mapper" |
| 2 | 🔌 **`create_engine`** | "The DB connection factory" |
| 3 | 📍 **`DATABASE_URL`** | "Where is the DB?" |
| 4 | 🏭 **`sessionmaker`** | "Build sessions on demand" |
| 5 | 🧱 **`declarative_base`** | "The parent of all models" |
| 6 | 📋 **`Column` and types** | "Define a column: type + constraints" |
| 7 | 🏷️ **`__tablename__`** | "The table name" |
| 8 | 🔑 **`primary_key=True`, `index=True`** | "Constraints on columns" |
| 9 | 🛠️ **`Base.metadata.create_all`** | "Actually create the tables" |
| 10 | 📦 **`Session`** | "The unit-of-work handle" |
| 11 | 🪝 **`yield` dependencies** | "Setup + teardown for sessions" |
| 12 | 🔄 **`db.add`, `db.commit`, `db.query`** | "The four CRUD ops" |
| 13 | 🆚 **SQLAlchemy 1.x vs 2.x** | "Old style vs new style" |
| 14 | 🔒 **Lazy initialization** | "Engine is created once" |
| 15 | 🧠 **Why use an ORM** | "Less SQL, more Python" |

---

## 📂 Project Structure

```
📁 A016_SQLAlchemy_Setup_Models_Database_Integration/
├── 🐍 main.py     ← 39 lines: engine, Base, Todo, get_db, one route
├── 🗄️ test.db     ← created on first run (SQLite database)
└── 📖 README.md   ← you are here
```

> ⚠️ `test.db` should be `.gitignore`d in real projects. It's a runtime artifact, not source.

---

## ⚙️ Installation & Setup

```powershell
cd D:\AllProgram\LEARN\Python\FastAPI\A016_SQLAlchemy_Setup_Models_Database_Integration
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "fastapi[standard]" sqlalchemy
```

> 🧠 **New dependency:** `sqlalchemy` is **not** part of `fastapi[standard]`. Install it explicitly.

Verify the install:

```powershell
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
# Should print: 2.x.x
```

Run the server:

```powershell
uvicorn main:app --reload
```

A `test.db` file appears — that's your SQLite database with a `todos` table inside.

---

## 🧬 Anatomy of `main.py` — Line by Line

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import FastAPI, Depends

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"

# Create database connection
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

session_local = sessionmaker(bind=engine)

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home(db: Session = Depends(get_db)):
    return {
        "message": "DB Connected fine"
    }
```

| Lines | Code | 🧠 Why it's there |
|:-----:|:-----|:------------------|
| 1–2 | `from sqlalchemy ...` | Import SQLAlchemy pieces |
| 5 | `app = FastAPI()` | App instance |
| 7 | `DATABASE_URL = "sqlite:///./test.db"` | **Where** the DB lives |
| 10–13 | `engine = create_engine(...)` | **The connection factory** |
| 15 | `session_local = sessionmaker(bind=engine)` | **Session factory** |
| 17 | `Base = declarative_base()` | **Parent class** for all models |
| 19–24 | `class Todo(Base)` | **Model** = a Python class that maps to a table |
| 26 | `Base.metadata.create_all(bind=engine)` | **Create the tables** in the DB |
| 28–33 | `def get_db()` | **Per-request session** via `yield` |
| 35–38 | `@app.get("/")` with `Depends(get_db)` | Verify connection |

### The 7 Mandatory Pieces

```python
DATABASE_URL = "..."        # 1. Where
engine = create_engine(...) # 2. Connection factory
session_local = sessionmaker(...)  # 3. Session factory
Base = declarative_base()  # 4. Model parent
class Todo(Base): ...       # 5. A model
Base.metadata.create_all(...)  # 6. Build tables
def get_db(): yield ...     # 7. Per-request session
```

> 🧠 **Mnemonic:** "**U-E-S-B-M-C-Y**" — **U**rl, **E**ngine, **S**ession, **B**ase, **M**odel, **C**reate, **Y**ield.

### 🎯 If you remember ONE thing
> **Define tables as Python classes inheriting from `Base`. SQLAlchemy creates the actual SQL tables when you call `Base.metadata.create_all(...)`.**

---

## 🛣️ API Endpoints

| Method | Endpoint | Purpose |
|:------:|:---------|:--------|
| 🟢 GET | `/` | Confirms the DB connection works |

The current app verifies the setup. Adding CRUD is in the *Variations* section below.

---

## 🧠 The Mental Model: 5 Layers of SQLAlchemy

```mermaid
flowchart TD
    A[Your Python class: Todo] -->|inheritance| B[declarative_base: Base]
    B -->|metadata| C[Base.metadata: list of all tables]
    C -->|create_all| D[engine: talks to the DB]
    D -->|via sessionmaker| E[Session: unit of work]
    E -->|via Depends| F[Per-request db handle]
    F -->|in your route| G[db.add, db.query, db.commit]
```

| Layer | What it is | Code |
|:------|:-----------|:-----|
| 1️⃣ **Model** | Python class = table | `class Todo(Base)` |
| 2️⃣ **Base** | Parent of all models | `Base = declarative_base()` |
| 3️⃣ **Metadata** | Registry of all tables | `Base.metadata` |
| 4️⃣ **Engine** | Talks to the actual DB | `create_engine(...)` |
| 5️⃣ **Session** | Your handle to query/save | `session_local()` |

> 🧠 **Mnemonic:** "**M-B-M-E-S**" → **M**odel, **B**ase, **M**etadata, **E**ngine, **S**ession. Top-to-bottom.

---

## 🆕 Every New Keyword & Function Explained

### 1. `create_engine(...)` — the connection factory

**What:** Creates an **engine** — a Python object that knows how to talk to your specific database (SQLite, PostgreSQL, MySQL, etc.).

**Signature:**
```python
create_engine(url, **kwargs)
```

| Argument | Meaning |
|:---------|:--------|
| `url` | Connection string (e.g., `sqlite:///./test.db`) |
| `connect_args` | Extra args for the DB driver (SQLite needs `check_same_thread=False` for FastAPI) |
| `echo` | If `True`, prints all SQL to stdout (debugging) |

**Returns:** an `Engine` object.

```python
engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
engine = create_engine("postgresql://user:pass@localhost/mydb")
```

> 🧠 **Mnemonic:** "**`create_engine` = the translator factory**."

### 2. `DATABASE_URL` — where the DB lives

**What:** A **connection string** that tells SQLAlchemy which database to use and how to connect.

| Prefix | Database | Example |
|:-------|:---------|:--------|
| `sqlite:///` | SQLite (file or in-memory) | `sqlite:///./test.db` |
| `postgresql://` | PostgreSQL | `postgresql://user:pass@localhost/mydb` |
| `mysql://` | MySQL | `mysql://user:pass@localhost/mydb` |

> **Note:** `sqlite:///./test.db` has **three** slashes — the third `/` is the start of the file path.

> 🧠 **Mnemonic:** "**Three slashes = SQLite file path.**"

### 3. `sessionmaker(bind=engine)` — session factory

**What:** Returns a **class** (not an instance!) that you can call to create new sessions.

```python
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()    # ← create a session
```

By convention, the variable is named `SessionLocal` (with capital S) and the **instance** is `db`.

> 🧠 **Mnemonic:** "**`sessionmaker` = cookie-cutter. `SessionLocal()` = a cookie.**"

### 4. `declarative_base()` — the model parent

**What:** Returns a **base class**. All your models inherit from it.

```python
Base = declarative_base()    # call it ONCE, at module level

class Todo(Base):            # inherit
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
```

`Base` is the registry that:
- Collects all model classes
- Knows their table names
- Provides `Base.metadata` (used to create the actual tables)

> 🧠 **Mnemonic:** "**`Base` = the family tree. All models are its children.**"

### 5. `class Todo(Base)` — the model

**What:** A Python class that maps to a database table.

```python
class Todo(Base):
    __tablename__ = "todos"           # ← table name in the DB

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(String)
```

| Piece | What it does |
|:------|:-------------|
| `__tablename__` | Tells SQLAlchemy the **table name** |
| `id = Column(Integer, primary_key=True)` | **Primary key** column |
| `index=True` | Create a **DB index** for fast lookup |
| `Column(String)` | A string column (VARCHAR) |

> 🧠 **Mnemonic:** "**`__tablename__` = table name. `Column` = column. **`"

### 6. `Column` — define a column

**Signature:**
```python
Column(type, *args, **kwargs)
```

| Argument | Meaning | Example |
|:---------|:--------|:--------|
| `Integer` / `String` / `Float` / `Boolean` / `DateTime` | Column type | `Column(Integer)` |
| `primary_key=True` | This column is the PK | `Column(Integer, primary_key=True)` |
| `index=True` | Create a DB index | `Column(String, index=True)` |
| `nullable=False` | Disallow NULL | `Column(String, nullable=False)` |
| `default=...` | Default value | `Column(String, default="pending")` |
| `unique=True` | Must be unique | `Column(String, unique=True)` |

```python
title = Column(String, nullable=False, default="untitled")
```

> 🧠 **Mnemonic:** "**Column = type + constraints**."

### 7. `Base.metadata.create_all(bind=engine)` — build the tables

**What:** Reads every model that inherits from `Base` and creates the corresponding tables in the DB.

```python
Base.metadata.create_all(bind=engine)
```

**Returns:** `None`. Side effect: tables now exist in the DB.

> ⚠️ **Idempotent:** Running it twice doesn't error — only creates tables that don't exist.

> 🧠 **Mnemonic:** "**create_all = 'build the missing tables now'**."

### 8. `Session` — your handle

**What:** A **session** represents a "unit of work" — a series of operations you'll commit or roll back together.

```python
db = SessionLocal()         # start a session
db.add(todo)                # stage a write
db.commit()                 # save everything
db.close()                  # end the session
```

A session also wraps **queries**:

```python
# SQLAlchemy 1.x style (still works)
db.query(Todo).all()
db.query(Todo).filter_by(id=1).first()

# SQLAlchemy 2.x style (recommended)
db.execute(select(Todo)).scalars().all()
db.execute(select(Todo).where(Todo.id == 1)).scalar()
```

> 🧠 **Mnemonic:** "**Session = shopping cart. `add` = put in. `commit` = checkout. `close` = leave.**"

### 9. `yield` dependencies — `get_db()`

**What:** A FastAPI dependency that creates a session **per request** and closes it after.

```python
def get_db():
    db = session_local()
    try:
        yield db            # ← route runs here, db is injected
    finally:
        db.close()          # ← always close, even on errors
```

**Why use `yield`?** Because you need **setup** (create session) AND **teardown** (close session). The `try/finally` ensures the session is always closed, even if the route raises.

> 🧠 **Mnemonic:** "**yield = setup + teardown.**"

### 10. `Depends(get_db)` — inject the session

**What:** FastAPI runs `get_db()` and passes the result to your route:

```python
@app.get("/")
def home(db: Session = Depends(get_db)):
    # db is a fresh SessionLocal() for THIS request
    ...
```

> 🧠 **Mnemonic:** "**Depends = 'give me a session per request'**."

---

## 🆚 Raw `sqlite3` (A015) vs SQLAlchemy (A016)

| Aspect | A015 (raw `sqlite3`) | A016 (SQLAlchemy) |
|:-------|:---------------------|:------------------|
| Define schema | `CREATE TABLE` SQL | Python `class` |
| Insert | `cursor.execute("INSERT ...")` | `db.add(obj); db.commit()` |
| Read | `cursor.fetchall()` | `db.query(Model).all()` |
| Update | `cursor.execute("UPDATE ...")` | `obj.field = new; db.commit()` |
| Delete | `cursor.execute("DELETE ...")` | `db.delete(obj); db.commit()` |
| Port to PostgreSQL | Rewrite all SQL | Just change `DATABASE_URL` |
| Type safety | None (returns tuples) | Full (returns objects) |
| Migrations | Manual | Alembic (separate tool) |

> 🧠 **Mnemonic:** "**Raw `sqlite3` = craft. SQLAlchemy = factory.**"

### The Same App, Two Ways

| Task | Raw `sqlite3` | SQLAlchemy |
|:-----|:--------------|:-----------|
| Add a row | `cursor.execute("INSERT INTO todos (title) VALUES (?)", ("Buy milk",))` | `db.add(Todo(title="Buy milk")); db.commit()` |
| Read all | `cursor.execute("SELECT * FROM todos").fetchall()` | `db.query(Todo).all()` |
| Read one | `cursor.execute("SELECT * FROM todos WHERE id = ?", (1,)).fetchone()` | `db.query(Todo).filter(Todo.id == 1).first()` |

---

## 🔧 Variations: Add Full CRUD with SQLAlchemy

Extend `main.py` with the standard 5 endpoints:

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import select
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(String, default="false")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TodoIn(BaseModel):
    title: str
    completed: str = "false"

class TodoOut(BaseModel):
    id: int
    title: str
    completed: str
    class Config:
        from_attributes = True   # ← Pydantic v2: read from SQLAlchemy attrs

@app.get("/todos")
def list_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

@app.post("/todos", status_code=201)
def create_todo(todo: TodoIn, db: Session = Depends(get_db)):
    obj = Todo(**todo.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(404, "Todo not found")
    return todo

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoIn, db: Session = Depends(get_db)):
    obj = db.query(Todo).filter(Todo.id == todo_id).first()
    if not obj:
        raise HTTPException(404, "Todo not found")
    obj.title = todo.title
    obj.completed = todo.completed
    db.commit()
    return obj

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    obj = db.query(Todo).filter(Todo.id == todo_id).first()
    if not obj:
        raise HTTPException(404, "Todo not found")
    db.delete(obj)
    db.commit()
    return None
```

### The Four CRUD Operations

| Operation | Method | Code |
|:----------|:-------|:-----|
| **C**reate | `db.add` | `db.add(obj); db.commit(); db.refresh(obj)` |
| **R**ead | `db.query` | `db.query(Model).all()` or `.filter(...).first()` |
| **U**pdate | mutate | `obj.field = new; db.commit()` |
| **D**elete | `db.delete` | `db.delete(obj); db.commit()` |

> 🧠 **Mnemonic:** "**Add-Commit-Refresh for create. Mutate-Commit for update. Delete-Commit for delete.**"

---

## 🧪 Try It With curl + Python REPL

### 1. Start the server

```powershell
uvicorn main:app --reload
```

### 2. Verify the connection

```bash
curl http://127.0.0.1:8000/
```

```json
{"message": "DB Connected fine"}
```

### 3. Inspect the schema from Python

```powershell
python -c "from sqlalchemy import create_engine, inspect; e = create_engine('sqlite:///./test.db'); print(inspect(e).get_columns('todos'))"
```

Output:

```
[{'name': 'id', 'type': INTEGER(), ...},
 {'name': 'title', 'type': VARCHAR(), ...},
 {'name': 'completed', 'type': VARCHAR(), ...}]
```

### 4. Query the empty table

```powershell
python -c "from main import SessionLocal, Todo; db = SessionLocal(); print(db.query(Todo).all()); db.close()"
```

Output: `[]` (empty — no rows yet).

### 5. Insert a row using SQLAlchemy

```powershell
python -c "from main import SessionLocal, Todo; db = SessionLocal(); db.add(Todo(title='Learn SQLAlchemy', completed='false')); db.commit(); db.close()"
```

Now `db.query(Todo).all()` returns `[(1, 'Learn SQLAlchemy', 'false')]`.

---

## ⚠️ Common Pitfalls & Fixes

| 😖 Pitfall | 🔍 Cause | ✅ Fix |
|:-----------|:---------|:------|
| `sqlalchemy.exc.OperationalError: no such table` | `create_all()` not called or called on wrong engine | Call `Base.metadata.create_all(bind=engine)` |
| `sqlite3.ProgrammingError: ... different thread` | Forgot `connect_args={"check_same_thread": False}` | Add it to `create_engine` |
| `DetachedInstanceError` after closing session | Used the object after `db.close()` | Keep the session open (via dependency) or use `db.expire_on_commit=False` |
| `NameError: name 'Base' is not defined` | Forgot `Base = declarative_base()` | Add it once at module level |
| `sqlalchemy.exc.ArgumentError: ...` | Wrong `DATABASE_URL` format | Check slashes (`sqlite:///./test.db` has 3) |
| Two `create_engine` instances talking to the same DB | Engine and session on different `Base` | Always use one `Base`, one `engine` |
| Pydantic can't serialize SQLAlchemy object | Missing `from_attributes = True` (Pydantic v2) | Add to `class Config` or use `model_config` |

### The Classic Pydantic + SQLAlchemy Fix (Pydantic v2)

```python
from pydantic import BaseModel

class TodoOut(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True    # ← tells Pydantic to read .id, .title from obj
```

Or with Pydantic v2 syntax:

```python
from pydantic import ConfigDict

class TodoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
```

> 🧠 **Mnemonic:** "**`from_attributes = True` = 'read from Python objects, not just dicts'**."

### `DetachedInstanceError` Explained

After `db.close()`, the object loses its connection to the DB. Accessing lazy-loaded fields throws this error. Two fixes:

```python
# Option 1: refresh before close
db.commit()
db.refresh(obj)    # ← load all attributes now
db.close()
# Now `obj.title` works

# Option 2: keep session open
return db.query(Todo).all()    # FastAPI serializes the response before close
```

---

## 🧠 Mnemonic Cheat Sheet

| Concept | Mnemonic | Story |
|:--------|:---------|:------|
| 7 setup steps | **U-E-S-B-M-C-Y** | Url, Engine, Session, Base, Model, Create, Yield |
| 5 layers | **M-B-M-E-S** | Model, Base, Metadata, Engine, Session |
| Connection string | **3 slashes = SQLite file** | `sqlite:///./test.db` |
| `Base` | **Family tree** | All models are children |
| `Column` | **Type + constraints** | `Column(String, nullable=False)` |
| `Session` | **Shopping cart** | add → commit → close |
| `yield` dep | **Setup + teardown** | Open before, close after |
| CRUD ops | **Add, Mutate, Delete, Query** | All followed by `db.commit()` |

---

## 🧪 Recall Test

1. What does `create_engine` do?
2. Why does SQLite need `connect_args={"check_same_thread": False}`?
3. What does `declarative_base()` return?
4. What's the role of `__tablename__`?
5. What's the difference between `sessionmaker` and `SessionLocal()`?
6. What does `Base.metadata.create_all(...)` do?
7. Why use `yield` in `get_db()` instead of `return`?
8. How do you query all rows of a `Todo` table?

> 8/8 → SQLAlchemy is yours.

---

## 🎯 Interview Q&A

### Q1: What is an ORM?

**Answer:** **Object-Relational Mapper.** A library that maps database tables to Python classes and rows to objects. You write Python, the ORM generates SQL.

| Without ORM | With ORM |
|:------------|:---------|
| `cursor.execute("INSERT INTO todos (title) VALUES (?)", ("Buy milk",))` | `db.add(Todo(title="Buy milk"))` |
| `cursor.fetchall()` → tuples | `db.query(Todo).all()` → objects |

> **One-liner:** *"ORM = bridge between Python objects and SQL tables."*

### Q2: What's the difference between `create_engine` and `sessionmaker`?

**Answer:**

| `create_engine` | `sessionmaker` |
|:----------------|:---------------|
| The **connection factory** | The **session factory** |
| One per app | One per app |
| Talks to the DB | Creates Session objects |
| Low-level | High-level |

```python
engine = create_engine("sqlite:///./test.db")    # the door
SessionLocal = sessionmaker(bind=engine)         # the cookie-cutter
db = SessionLocal()                              # a cookie (session)
```

> **One-liner:** *"Engine = connection. SessionLocal = session builder. Session = your handle."*

### Q3: What's `declarative_base()` and why do you call it once?

**Answer:** `declarative_base()` returns a base class. All your models inherit from it. SQLAlchemy needs this base to:

- Register every model that inherits from it
- Collect their table definitions in `Base.metadata`
- Build the actual tables via `Base.metadata.create_all(...)`

Calling it once ensures one shared registry. Calling it twice creates two disconnected class families.

> **One-liner:** *"Base = the registry of all your models. One app, one Base."*

### Q4: What's the difference between `Column(Integer, primary_key=True)` and `Column(Integer, primary_key=True, index=True)`?

**Answer:**

| Option | Effect |
|:-------|:-------|
| `primary_key=True` | Marks the column as the table's primary key (unique, not null) |
| `index=True` | Creates a database **index** on this column for faster lookups |

The primary key **already** needs to be unique, but `index=True` adds a separate index for queries like `WHERE id = ?`. Common on columns you query often.

> **One-liner:** *"PK = unique identity. `index=True` = fast lookups."*

### Q5: Why use `yield` in `get_db()` instead of `return`?

**Answer:** `yield` lets you run code **before AND after** the route handler:

```python
def get_db():
    db = SessionLocal()       # setup: create session
    try:
        yield db              # route runs here
    finally:
        db.close()            # teardown: always close
```

With `return db`, you'd have no teardown — sessions would leak, and the DB connection wouldn't be released. The `try/finally` ensures cleanup even if the route raises.

> **One-liner:** *"yield = setup before, teardown after. Always close, even on errors."*

### Q6: How do you switch from SQLite to PostgreSQL?

**Answer:** Just change the `DATABASE_URL`:

```python
# SQLite
DATABASE_URL = "sqlite:///./test.db"

# PostgreSQL
DATABASE_URL = "postgresql://user:pass@localhost/mydb"
```

And add the driver:

```powershell
pip install psycopg2-binary
```

The model code (`class Todo(Base)`) stays the same. SQLAlchemy writes the right SQL for each dialect.

> **One-liner:** *"Change one URL, port to any DB. That's the ORM win."*

### Q7: What's the difference between `db.query(Model)` and `db.execute(select(Model))`?

**Answer:**

| Style | Version | Example |
|:------|:--------|:--------|
| Legacy (1.x) | SQLAlchemy 1.x | `db.query(Todo).filter(Todo.id == 1).first()` |
| Modern (2.x) | SQLAlchemy 2.0+ | `db.execute(select(Todo).where(Todo.id == 1)).scalar()` |

The 2.x style is more explicit and matches Python's `select` syntax.

> **One-liner:** *"1.x = `db.query`. 2.x = `db.execute(select(...))`."*

### Q8: Why use `db.refresh(obj)` after `db.add` and `db.commit()`?

**Answer:** After committing, the in-memory object might not have the values the database generated (e.g., auto-incremented `id`, default timestamps). `db.refresh(obj)` re-queries the row to populate those fields:

```python
db.add(Todo(title="x"))    # obj.id is None
db.commit()                # row inserted, id assigned in DB
db.refresh(obj)            # obj.id is now 1 (the DB-assigned value)
print(obj.id)              # 1
```

> **One-liner:** *"refresh = 'load what the DB just generated'."*

---

## 🚀 Where to Go Next

| Direction | Module |
|:----------|:-------|
| ⬅️ Previous | [A015](../A015_SQLite_Database_Integration_Setup_SQLAlchemy_Intro/) |
| ⬅️ Back | [Root README](../README.md) |
| ➡️ Next | A017 (planned) — Alembic migrations + relationships |
| ➡️ Future | A018 (planned) — Async SQLAlchemy 2.0 |

---

<div align="center">

### 🏛️ *Tables as classes. Queries as Python. That's SQLAlchemy.* 🏛️

Made with ❤️, a `Base` class, and a `SessionLocal`.

</div>