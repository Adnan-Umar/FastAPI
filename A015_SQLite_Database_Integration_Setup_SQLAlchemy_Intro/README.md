<div align="center">

# 🗄️ A015 — SQLite Database Integration: Setup & `sqlite3` Intro

### *Persist your data. Survive server restarts. Speak SQL.*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-✅-blue?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Level-Advanced-red?style=for-the-badge)
![Reading Time](https://img.shields.io/badge/Read_Time-60_min-blueviolet?style=for-the-badge)
![Lines of Code](https://img.shields.io/badge/Lines_of_Code-24-informational?style=for-the-badge)

</div>

---

## 🧠 The One-Sentence Summary

> **SQLite is a server-less, file-based database; `sqlite3` is Python's built-in module that lets you open a `.db` file, get a `cursor`, and run SQL — all without installing anything extra.**

If you remember *"sqlite3 = file + cursor + SQL"*, the rest of this README is decoration.

---

## 📑 Table of Contents

- [🧠 The One-Sentence Summary](#-the-one-sentence-summary)
- [📖 The Story: The Filing Cabinet](#-the-story-the-filing-cabinet)
- [🎯 What You Will Learn (15 Skills — heavy module)](#-what-you-will-learn-15-skills--heavy-module)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧬 Anatomy of `main.py` — Line by Line](#-anatomy-of-mainpy--line-by-line)
- [🛣️ API Endpoints](#-api-endpoints)
- [🧠 The Mental Model: How SQLite Works](#-the-mental-model-how-sqlite-works)
- [🆕 Every New Keyword & Function Explained](#-every-new-keyword--function-explained)
- [🆕 SQL Refresher — The 6 Commands You Need](#-sql-refresher--the-6-commands-you-need)
- [🧪 Try It With curl + Python REPL](#-try-it-with-curl--python-repl)
- [🛡️ SQL Injection — The #1 Threat (and the Fix)](#-sql-injection--the-1-threat-and-the-fix)
- [🆚 `sqlite3` vs SQLAlchemy vs ORMs](#-sqlite3-vs-sqlalchemy-vs-orms)
- [🔧 Variations: Add Full CRUD to This App](#-variations-add-full-crud-to-this-app)
- [⚠️ Common Pitfalls & Fixes](#-common-pitfalls--fixes)
- [🧠 Mnemonic Cheat Sheet](#-mnemonic-cheat-sheet)
- [🧪 Recall Test](#-recall-test)
- [🎯 Interview Q&A](#-interview-qa)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 📖 The Story: The Filing Cabinet

Imagine your data lives in a **filing cabinet** 🗄️. So far in this course, your "cabinet" was a Python list (lost on restart). Now we're upgrading to a real cabinet:

| Old | New |
|:----|:----|
| Python `list` | **SQLite `.db` file** |
| In-memory | **On disk** (survives restarts) |
| Lost on crash | **Durable** (transaction-safe) |
| No query language | **SQL** (Structured Query Language) |
| One process only | **Shared** (with locking) |

The "filing cabinet" has **drawers** (tables), each with **folders** (rows) holding **fields** (columns). The `sqlite3` module is the **librarian** that lets you open drawers, add folders, and search.

> 🧠 **Mnemonic:** "**SQLite = cabinet. Table = drawer. Row = folder. Column = field.**"

---

## 🎯 What You Will Learn (15 Skills — heavy module)

| # | 🎯 Skill | 🧠 You'll remember it because... |
|:-:|:---------|:--------------------------------|
| 1 | 🗄️ **What SQLite is** | "Server-less, file-based DB" |
| 2 | 📥 **The `sqlite3` module** | "Built into Python's stdlib" |
| 3 | 🔌 **`sqlite3.connect()`** | "Open the file" |
| 4 | 🖱️ **`cursor()` method** | "Your SQL execution handle" |
| 5 | ⚡ **`cursor.execute()`** | "Run one SQL statement" |
| 6 | 💾 **`conn.commit()`** | "Save changes" |
| 7 | 🔓 **`check_same_thread=False`** | "Let FastAPI's threads share it" |
| 8 | 📊 **SQL: `CREATE TABLE`** | "Define schema" |
| 9 | 🔑 **`PRIMARY KEY`** | "Unique id per row" |
| 10 | 📝 **SQL types: `INTEGER`, `TEXT`** | "Column types" |
| 11 | 🔍 **`IF NOT EXISTS`** | "Don't crash if table already exists" |
| 12 | 🛡️ **Parameterized queries (`?`)** | "Prevent SQL injection" |
| 13 | 🆚 **`?` vs `%s` vs `:name`** | "DB-API parameter styles" |
| 14 | 🧠 **ACID transactions** | "Atomic, Consistent, Isolated, Durable" |
| 15 | 🔄 **Auto-commit vs manual** | "Why `commit()` matters" |

---

## 📂 Project Structure

```
📁 A015_SQLite_Database_Integration_Setup_SQLAlchemy_Intro/
├── 🐍 main.py     ← 24 lines: opens DB, creates table, one route
├── 🗄️ test.db     ← created on first run (SQLite database file)
└── 📖 README.md   ← you are here
```

> ⚠️ `test.db` is a **runtime artifact** — created when you start the server. It should be in `.gitignore` for real projects, but is tracked here for learning.

---

## ⚙️ Installation & Setup

**Zero extra installs.** `sqlite3` ships with Python.

```powershell
cd D:\AllProgram\LEARN\Python\FastAPI\A015_SQLite_Database_Integration_Setup_SQLAlchemy_Intro
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "fastapi[standard]"
uvicorn main:app --reload
```

After the first run, you'll see `test.db` in the folder. To inspect it:

```powershell
# Option 1: Python REPL
python -c "import sqlite3; c = sqlite3.connect('test.db').cursor(); print(c.execute('SELECT * FROM todos').fetchall())"

# Option 2: DB Browser for SQLite (GUI, free)
# Download: https://sqlitebrowser.org

# Option 3: sqlite3 CLI (if installed)
sqlite3 test.db ".schema"
```

> 💡 `test.db` should be added to `.gitignore` in a real project — databases are not source code.

---

## 🧬 Anatomy of `main.py` — Line by Line

```python
import sqlite3
from fastapi import FastAPI

app = FastAPI()

conn = sqlite3.connect("test.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS todos(
            id INTEGER PRIMARY KEY,
            title TEXT,
            completed TEXT
        )
""");

conn.commit()

@app.get("/")
def home():
    return {
        "message": "SQLite connected fine"
    }
```

| Lines | Code | 🧠 Why it's there |
|:-----:|:-----|:------------------|
| 1 | `import sqlite3` | Built-in DB driver — no install needed |
| 3 | `app = FastAPI()` | App instance |
| 6 | `conn = sqlite3.connect("test.db", check_same_thread=False)` | **Open** the file (creates if missing) |
| 8 | `cursor = conn.cursor()` | **Get a cursor** to run SQL |
| 10–16 | `cursor.execute("CREATE TABLE IF NOT EXISTS ...")` | **Define schema** |
| 18 | `conn.commit()` | **Save** the schema to disk |
| 20–23 | `GET /` | Verify the DB is connected |

### The Four-Step Pattern

```python
conn = sqlite3.connect(...)     # 1. Connect
cursor = conn.cursor()          # 2. Get cursor
cursor.execute("SQL ...")       # 3. Run SQL
conn.commit()                   # 4. Save (for writes)
```

> 🧠 **Mnemonic:** "**C-C-E-C**" — **C**onnect, **C**ursor, **E**xecute, **C**ommit. (Or "**4C's of SQLite**".)

### 🎯 If you remember ONE thing
> **`sqlite3` gives you `conn` and `cursor`. `cursor.execute(...)` runs SQL. `conn.commit()` saves writes. That's the whole API.**

---

## 🛣️ API Endpoints

| Method | Endpoint | Purpose |
|:------:|:---------|:--------|
| 🟢 GET | `/` | Sanity check — confirms DB is connected |

The current app only verifies the connection. Adding CRUD is in the *Variations* section below.

---

## 🧠 The Mental Model: How SQLite Works

```
┌────────────────────────────────────────────┐
│  Your Python process                        │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │  sqlite3 module                      │  │
│  │                                      │  │
│  │  Connection (conn) ── represents ──► │  │
│  │  Cursor (cursor) ── executes ────►  │  │
│  │                                      │  │
│  └────────────┬─────────────────────────┘  │
│               │                            │
│               ▼                            │
│  ┌──────────────────────────────────────┐  │
│  │  test.db (file on disk)              │  │
│  │                                      │  │
│  │  ┌────────────┐                      │  │
│  │  │  todos     │  ← table             │  │
│  │  ├────────────┤                      │  │
│  │  │ id │ title │ completed            │  │
│  │  │ ───┼───────┼──────────            │  │
│  │  │  1 │ buy   │ false                │  │
│  │  │  2 │ read  │ true                 │  │
│  │  └────────────┘                      │  │
│  └──────────────────────────────────────┘  │
└────────────────────────────────────────────┘
```

> 🧠 **Mnemonic:** "**Connection = door. Cursor = hand. SQL = command. DB = filing cabinet.**"

---

## 🆕 Every New Keyword & Function Explained

This module introduces a lot of new vocabulary. Here's every single one, defined in plain English.

### 1. `import sqlite3` — the module

**What:** Python's built-in driver for SQLite. Part of the standard library — no `pip install` needed.

**Why:** Python ships with SQLite bindings. Anything you need to talk to a `.db` file is already on your machine.

```python
import sqlite3    # the whole module
from sqlite3 import connect, IntegrityError    # specific names
```

> 🧠 **Mnemonic:** "**`sqlite3` = SQLite + Python version 3**" (the module name also matches Python 3).

### 2. `sqlite3.connect(database, ...)` — the function

**Signature:**
```python
sqlite3.connect(database, timeout=5.0, detect_types=0,
               isolation_level="", check_same_thread=True,
               factory=None, cached_statements=128, uri=False)
```

**What it does:** Opens (or creates) a connection to a SQLite database.

| Argument | Meaning |
|:---------|:--------|
| `database` | File path (`"test.db"`) or `":memory:"` for in-memory |
| `check_same_thread` | `True` (default) = only the thread that created the conn can use it. `False` = any thread can. |
| `timeout` | Seconds to wait when the DB is locked |
| `isolation_level` | Transaction mode (default is "deferred") |

**Returns:** a `Connection` object.

```python
# File-based
conn = sqlite3.connect("test.db")

# In-memory (lost when closed)
conn = sqlite3.connect(":memory:")

# Thread-safe (needed for FastAPI)
conn = sqlite3.connect("test.db", check_same_thread=False)
```

> 🧠 **Mnemonic:** "**`connect` = open the door**."

### 3. `conn.cursor()` — get an executor

**What:** Returns a `Cursor` object — your handle for running SQL and reading results.

**Why:** A connection can have multiple cursors, but you only need one per "thread of work".

```python
cursor = conn.cursor()
```

> 🧠 **Mnemonic:** "**`cursor` = the hand that holds the pen**."

### 4. `cursor.execute(sql, parameters)` — run a statement

**Signature:**
```python
cursor.execute(sql, parameters=())
```

**What it does:** Compiles and runs **one** SQL statement. Returns the cursor itself (so you can chain).

```python
cursor.execute("CREATE TABLE users (id INTEGER, name TEXT)")
cursor.execute("INSERT INTO users VALUES (?, ?)", (1, "Adnan"))
```

**Two flavors:**

| Style | Example | Notes |
|:------|:--------|:------|
| Plain string | `cursor.execute("SELECT 1")` | Risky if user input is involved |
| Parameterized | `cursor.execute("SELECT * FROM users WHERE id = ?", (42,))` | **Safe** — uses placeholders |

> 🧠 **Mnemonic:** "**`execute` = run the command**."

### 5. `cursor.executemany(sql, seq_of_params)` — run many

**What:** Runs the same SQL once per item in a sequence. **Huge speedup** for bulk inserts.

```python
todos = [(1, "Buy milk"), (2, "Read book"), (3, "Sleep")]
cursor.executemany("INSERT INTO todos (id, title) VALUES (?, ?)", todos)
conn.commit()
```

> 🧠 **Mnemonic:** "**`executemany` = execute N times in one call**."

### 6. `cursor.fetchone()`, `fetchall()`, `fetchmany(n)`

**What:** Read the results of a `SELECT`.

| Method | Returns |
|:-------|:--------|
| `fetchone()` | Next row, or `None` |
| `fetchall()` | List of all remaining rows |
| `fetchmany(n)` | List of next `n` rows |

```python
cursor.execute("SELECT * FROM todos")
print(cursor.fetchone())    # (1, 'Buy milk', 'false')
print(cursor.fetchall())    # [(2, 'Read book', 'true'), (3, 'Sleep', 'false')]
```

> 🧠 **Mnemonic:** "**fetchone = one row. fetchall = all rows.**"

### 7. `conn.commit()` — save writes

**What:** Persists all pending changes to the database file.

**Why:** SQLite (and most DBs) use **transactions**. Until you `commit()`, the changes are pending and could be rolled back.

| Operation | Needs `commit()`? |
|:----------|:------------------|
| `SELECT` | ❌ No (read-only) |
| `CREATE TABLE` | ✅ Yes (schema change) |
| `INSERT` / `UPDATE` / `DELETE` | ✅ Yes (data change) |
| `DROP TABLE` | ✅ Yes |

> 🧠 **Mnemonic:** "**commit = save the receipt**."

### 8. `conn.rollback()` — undo writes

**What:** Discards all pending changes since the last `commit()`.

```python
try:
    cursor.execute("INSERT INTO todos VALUES (?, ?)", (1, "x"))
    cursor.execute("INSERT INTO todos VALUES (?, ?)", (2, "y"))
    conn.commit()    # both saved
except Exception:
    conn.rollback()  # both discarded
```

> 🧠 **Mnemonic:** "**rollback = undo**."

### 9. `conn.close()` — close the connection

**What:** Closes the file handle. The DB is unreachable after this.

```python
conn.close()
```

**Best practice:** Use a `with` block or `try/finally` to ensure closure.

> 🧠 **Mnemonic:** "**close = shut the door**."

### 10. `check_same_thread=False` — the FastAPI flag

**What:** Allows multiple threads (which FastAPI uses for sync handlers) to share the same connection.

**Why:** SQLite's default is thread-safe only for the thread that created the connection. FastAPI runs route handlers in a thread pool, so the default would break.

| Setting | Behavior | Use when |
|:--------|:---------|:---------|
| `True` (default) | Only the creating thread can use the connection | Single-threaded scripts |
| `False` | Any thread can use it | FastAPI, async workers |

> 🧠 **Mnemonic:** "**`check_same_thread=False` = 'threads, share this'**."

---

## 🆕 SQL Refresher — The 6 Commands You Need

The `main.py` uses **one** SQL command: `CREATE TABLE`. Here are the rest you'll need for CRUD.

### 1. `CREATE TABLE` — define schema

```sql
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY,
    title TEXT,
    completed TEXT
);
```

| Part | Meaning |
|:-----|:--------|
| `IF NOT EXISTS` | Don't error if table already there |
| `id INTEGER PRIMARY KEY` | Auto-incrementing unique id |
| `title TEXT` | String column |
| `completed TEXT` | String column (use 0/1 or 'true'/'false') |

### 2. `INSERT` — add a row

```sql
INSERT INTO todos (id, title, completed) VALUES (1, 'Buy milk', 'false');
```

### 3. `SELECT` — read rows

```sql
-- All rows
SELECT * FROM todos;

-- Filtered
SELECT * FROM todos WHERE id = 1;

-- Sorted
SELECT * FROM todos ORDER BY id DESC;
```

### 4. `UPDATE` — modify a row

```sql
UPDATE todos SET completed = 'true' WHERE id = 1;
```

### 5. `DELETE` — remove a row

```sql
DELETE FROM todos WHERE id = 1;
```

### 6. `DROP TABLE` — delete the whole table

```sql
DROP TABLE IF EXISTS todos;
```

> 🧠 **Mnemonic:** "**C-I-S-U-D-D**" → **C**reate, **I**nsert, **S**elect, **U**pdate, **D**elete, **D**rop. The CRUDD of SQL.

---

## 🧪 Try It With curl + Python REPL

### 1. Start the server

```powershell
uvicorn main:app --reload
```

You should see `test.db` appear in the folder.

### 2. Verify with curl

```bash
curl http://127.0.0.1:8000/
```

```json
{"message": "SQLite connected fine"}
```

### 3. Inspect the table from the REPL

```powershell
python -c "import sqlite3; c = sqlite3.connect('test.db').cursor(); print(c.execute('SELECT * FROM todos').fetchall())"
```

Output: `[]` (empty — no rows yet).

### 4. Add a row manually

```powershell
python -c "import sqlite3; c = sqlite3.connect('test.db'); c.cursor().execute('INSERT INTO todos VALUES (1, \"Buy milk\", \"false\")'); c.commit(); c.close()"
```

### 5. Verify the row persists across restarts

Stop the server (Ctrl+C), restart it, and re-run step 3. The row is still there! 🎉

> 🧠 **Mnemonic:** "**Stop the server, data survives. That's persistence.**"

---

## 🛡️ SQL Injection — The #1 Threat (and the Fix)

### ❌ The Vulnerable Way (NEVER do this)

```python
name = input("Enter name: ")
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")
```

If `name = "'; DROP TABLE users; --"`, the SQL becomes:

```sql
SELECT * FROM users WHERE name = ''; DROP TABLE users; --'
```

Your table is **gone**. This is **SQL injection** — the #1 web vulnerability for 20+ years.

### ✅ The Safe Way (ALWAYS do this)

```python
cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
```

The driver **escapes** the input for you. The `?` is a **placeholder**.

| Placeholder style | Database | Example |
|:------------------|:---------|:--------|
| `?` | SQLite, MySQL, PostgreSQL (DB-API) | `WHERE id = ?` |
| `%s` | psycopg2 (old) | `WHERE id = %s` |
| `:name` | SQLAlchemy, named param | `WHERE id = :id` |

> 🧠 **Mnemonic:** "**Never f-string SQL. Always use `?`.**"

---

## 🆚 `sqlite3` vs SQLAlchemy vs ORMs

| Tool | Level | Pros | Cons |
|:-----|:------|:-----|:-----|
| **`sqlite3`** (raw) | Low | Zero install, total control | You write SQL by hand |
| **SQLAlchemy Core** | Mid | SQL expression language, type-safe | More setup |
| **SQLAlchemy ORM** | High | Python objects = tables | Learning curve |
| **Tortoise ORM** | High | Async-first | Smaller community |
| **SQLModel** | High | SQLAlchemy + Pydantic combined | Newer |

### When to Use What

| Stage | Use |
|:------|:----|
| Learning / small scripts | Raw `sqlite3` ← **this module** |
| Production single-app | SQLAlchemy + Alembic (migrations) |
| Async FastAPI | SQLAlchemy 2.0 async or SQLModel |
| Microservices | Tortoise ORM or SQLModel |

> 🧠 **Mnemonic:** "**Raw `sqlite3` = learning. SQLAlchemy = production. ORM = object-thinking.**"

---

## 🔧 Variations: Add Full CRUD to This App

Here's how to extend `main.py` with all five CRUD endpoints:

```python
import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

conn = sqlite3.connect("test.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos(
        id INTEGER PRIMARY KEY,
        title TEXT,
        completed TEXT
    )
""")
conn.commit()

class Todo(BaseModel):
    title: str
    completed: str = "false"

@app.get("/todos")
def list_todos():
    cursor.execute("SELECT * FROM todos")
    return {"todos": cursor.fetchall()}

@app.post("/todos", status_code=201)
def create_todo(todo: Todo):
    cursor.execute(
        "INSERT INTO todos (title, completed) VALUES (?, ?)",
        (todo.title, todo.completed)
    )
    conn.commit()
    return {"message": "created", "data": todo}

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(404, "Todo not found")
    return {"id": row[0], "title": row[1], "completed": row[2]}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
    cursor.execute(
        "UPDATE todos SET title = ?, completed = ? WHERE id = ?",
        (todo.title, todo.completed, todo_id)
    )
    conn.commit()
    return {"message": "updated"}

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    return None
```

### Why a Global `conn` Is a Bad Idea

This module uses a module-level connection for simplicity. In production, use a **per-request** connection via a dependency:

```python
from fastapi import Depends

def get_db():
    db = sqlite3.connect("test.db")
    try:
        yield db
    finally:
        db.close()

@app.get("/todos")
def list_todos(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM todos")
    return cursor.fetchall()
```

> 🧠 **Mnemonic:** "**Global conn = tutorial. `Depends(get_db)` = production.**"

---

## ⚠️ Common Pitfalls & Fixes

| 😖 Pitfall | 🔍 Cause | ✅ Fix |
|:-----------|:---------|:------|
| `sqlite3.ProgrammingError: SQLite objects created in a thread...` | Default `check_same_thread=True` | Add `check_same_thread=False` |
| Data lost on restart | Forgot `conn.commit()` | Always commit after writes |
| `cursor.fetchall()` returns `[]` | Wrong column name in `SELECT` | Double-check column names |
| `IntegrityError: UNIQUE constraint failed` | Tried to insert duplicate `PRIMARY KEY` | Use `AUTOINCREMENT` or check first |
| SQL injection | Used f-string in `execute()` | Use `?` placeholders |
| `test.db` is locked | Another process has it open (e.g., DB Browser) | Close the other tool |
| `database is locked` timeout | Two writes at the same time | Add `timeout=10` to `connect()` |

### Auto-incrementing IDs

```sql
-- Without AUTOINCREMENT, ids are reused after delete
CREATE TABLE todos (
    id INTEGER PRIMARY KEY,   -- ✅ auto-increments
    title TEXT
);
```

With `INTEGER PRIMARY KEY` and a NULL id, SQLite assigns the next id automatically:

```python
cursor.execute("INSERT INTO todos (title) VALUES (?)", ("Buy milk",))
# id is auto-assigned (1, 2, 3, ...)
```

### Adding a `created_at` Timestamp

```python
from datetime import datetime

cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos(
        id INTEGER PRIMARY KEY,
        title TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")
```

`CURRENT_TIMESTAMP` is an SQLite function that returns the current time in `YYYY-MM-DD HH:MM:SS` format.

---

## 🧠 Mnemonic Cheat Sheet

| Concept | Mnemonic | Story |
|:--------|:---------|:------|
| The 4 steps | **C-C-E-C** | Connect, Cursor, Execute, Commit |
| SQLite parts | **Cabinet / drawer / folder / field** | DB / table / row / column |
| CRUDD | **C-I-S-U-D-D** | Create, Insert, Select, Update, Delete, Drop |
| 4 gifts of `?` | **Safe, fast, typed, escaped** | Why placeholders beat f-strings |
| `check_same_thread` | **Threads, share this** | FastAPI flag |
| `commit` | **Save the receipt** | Without it, you lose changes |
| ACID | **Atomic, Consistent, Isolated, Durable** | Transaction guarantees |

---

## 🧪 Recall Test

1. What does `import sqlite3` give you? (No install needed?)
2. What does `sqlite3.connect()` return?
3. What is a `cursor` and what does it do?
4. What's the difference between `execute()` and `executemany()`?
5. Which operations need `commit()`?
6. Why use `?` placeholders instead of f-strings?
7. What does `check_same_thread=False` do?
8. What's the difference between `fetchone()` and `fetchall()`?

> 8/8 → SQLite + FastAPI is yours.

---

## 🎯 Interview Q&A

### Q1: What is SQLite and why is it useful for learning?

**Answer:** SQLite is a **server-less, file-based, ACID-compliant** database engine. It's bundled with Python so no install is needed. Perfect for:

- Learning SQL
- Small apps
- Prototyping
- Embedded systems (iOS, Android)

> **One-liner:** *"SQLite = database in a file. Zero setup, zero server."*

### Q2: Explain the difference between a `Connection` and a `Cursor`.

**Answer:**

| Connection (`conn`) | Cursor (`cursor`) |
|:--------------------|:------------------|
| Represents the **DB connection** | Represents a **SQL execution context** |
| One per database | One or more per connection |
| `commit()`, `rollback()`, `close()` | `execute()`, `fetchone()`, `fetchall()` |

> **One-liner:** *"Connection = the door. Cursor = the hand that runs SQL."*

### Q3: What is SQL injection and how do you prevent it?

**Answer:** SQL injection is when user input is concatenated into a SQL string, allowing the user to alter the query. **Always use parameterized queries**:

```python
# ❌ Vulnerable
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")

# ✅ Safe
cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
```

The driver escapes the input automatically.

> **One-liner:** *"Never f-string SQL. Always use `?` placeholders."*

### Q4: What does `conn.commit()` do, and what happens if you forget it?

**Answer:** `commit()` persists all pending writes to disk. If you forget:

- The data is **lost** when the connection closes
- A crash or rollback discards the changes

This is the **transaction** model: writes are pending until you commit.

> **One-liner:** *"`commit()` = save. Without it, you lose changes."*

### Q5: Why do you need `check_same_thread=False` for FastAPI?

**Answer:** By default, SQLite connections can only be used by the thread that created them. FastAPI runs sync route handlers in a **thread pool**, so the default would crash. Setting `check_same_thread=False` allows any thread to use the connection.

> **One-liner:** *"FastAPI uses multiple threads — let them all use the same DB connection."*

### Q6: What's the difference between `fetchone()`, `fetchmany(n)`, and `fetchall()`?

**Answer:**

| Method | Returns |
|:-------|:--------|
| `fetchone()` | The next row, or `None` if done |
| `fetchmany(n)` | The next `n` rows as a list |
| `fetchall()` | All remaining rows as a list |

> **One-liner:** *"fetchone = 1. fetchmany = n. fetchall = everything left."*

### Q7: What does `PRIMARY KEY` do in SQL?

**Answer:** `PRIMARY KEY` makes a column **unique and not null**. It's the row's identity. SQLite auto-increments `INTEGER PRIMARY KEY` if you don't provide a value:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,   -- auto-increments
    name TEXT
);
```

> **One-liner:** *"PRIMARY KEY = unique id. Auto-increments on INTEGER."*

### Q8: When would you use raw `sqlite3` vs SQLAlchemy?

**Answer:**

| Use raw `sqlite3` | Use SQLAlchemy |
|:------------------|:----------------|
| Small scripts | Production apps |
| One-off data analysis | Multi-table schemas |
| Learning SQL | Need migrations (Alembic) |
| Minimal dependencies | Want ORM (objects = tables) |

In production, SQLAlchemy is almost always the right choice.

> **One-liner:** *"Raw `sqlite3` = learning. SQLAlchemy = production."*

---

## 🚀 Where to Go Next

| Direction | Module |
|:----------|:-------|
| ⬅️ Previous | [A014](../A014_Middleware_Explained_Logging_Request_Response_Flow/) |
| ⬅️ Back | [Root README](../README.md) |
| ➡️ Next | A016 (planned) — SQLAlchemy ORM with Pydantic models |
| ➡️ Future | A017 (planned) — Database migrations with Alembic |

---

<div align="center">

### 🗄️ *From chalkboard to filing cabinet. Data that survives.* 🗄️

Made with ❤️, a `.db` file, and a `?` placeholder.

</div>