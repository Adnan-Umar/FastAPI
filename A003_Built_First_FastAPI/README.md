<div align="center">

# 🛣️ A003 — Building Your First FastAPI App

### *Three routes, one app — scaling up from Hello World*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Difficulty](https://img.shields.io/badge/Level-Beginner-brightgreen?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-blue?style=for-the-badge)
![Endpoints](https://img.shields.io/badge/Endpoints-3-orange?style=for-the-badge)

<br/>

> A small but meaningful step up from "Hello World". Three `GET` endpoints — *home*, *about*, and *users* — show how route ordering and handler naming affect URL matching.

</div>

---

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    🛣️  Three Routes, One App                                  ║
║                                                               ║
║    GET  /         Welcome to fastapi                          ║
║    GET  /about    This is about page                          ║
║    GET  /users    [Adnan, umar, Md]                           ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 📑 Table of Contents

- [🎯 What You Will Learn](#-what-you-will-learn)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧠 Anatomy of main.py](#-anatomy-of-mainpy)
- [🛣️ API Endpoints](#-api-endpoints)
- [🧪 Try It](#-try-it)
- [📐 HTTP & Routing Concepts](#-http--routing-concepts)
- [⚠️ Common Pitfalls](#-common-pitfalls)
- [🔧 Suggested Refactor](#-suggested-refactor)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 🎯 What You Will Learn

| # | Skill | Description |
|:-:|:------|:------------|
| 1 | 🛣️ **Multiple Routes** | Add several routes to one FastAPI app. |
| 2 | 🌐 **HTTP Verbs** | Understand the difference between `GET`, `POST`, etc. |
| 3 | 🔄 **Auto JSON** | Return values are auto-converted to JSON. |
| 4 | 🏷️ **Unique Names** | Why each handler must have a unique function name. |
| 5 | 📚 **Nested Dicts** | Return lists and nested dictionaries. |
| 6 | 🧪 **Test Endpoints** | Try them with `curl` or browser. |

---

## 📂 Project Structure

```
📁 A003_Built_First_FastAPI/
├── 🐍 main.py     # Three-route FastAPI app
└── 📖 README.md   # You are here
```

---

## ⚙️ Installation & Setup

```powershell
cd D:\AllProgram\LEARN\Python\FastAPI\A003_Built_First_FastAPI
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "fastapi[standard]"
uvicorn main:app --reload
```

Then open <http://127.0.0.1:8000/> in your browser.

---

## 🧠 Anatomy of `main.py`

```python
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
```

### 🔍 Line-by-Line Breakdown

| Line | Code | Explanation |
|:----:|:-----|:------------|
| 1 | `from fastapi import FastAPI` | Framework import. |
| 3 | `app = FastAPI()` | Creates the ASGI app. |
| 6–8 | `@app.get("/")` | Root route. Returns a simple welcome dict. |
| 11–13 | `@app.get("/about")` | Static route `/about`. FastAPI matches it exactly (case-sensitive). |
| 16–20 | `@app.get("/users")` | Returns a list of users. Note that the function is *also* named `about`! |

> ⚠️ **Gotcha:** Two handlers in the same file are both called `about`. Python will **silently overwrite** the first one. The endpoint `/about` still works, but `/users` is served by whichever function was registered last. Always give handler functions **unique names**, even when URLs differ.

### 🎯 Why three endpoints in one file?

This module shows how FastAPI lets you scale from "hello world" (A002) to a small but real API **without restructuring anything**. As your app grows you will split routes into **routers** (covered in later modules).

---

## 🛣️ API Endpoints

| Method | Endpoint | Description | Sample Response |
|:------:|:---------|:------------|:----------------|
| 🟢 **GET** | `/` | Welcome message | `{ "message": "Welcome to fastapi" }` |
| 🟢 **GET** | `/about` | About page message | `{ "message": "This is about page" }` |
| 🟢 **GET** | `/users` | Returns a hard-coded list | `{ "users": ["Adnan", "umar", "Md"] }` |

---

## 🧪 Try It

### 🌐 Browser

```
http://127.0.0.1:8000/
http://127.0.0.1:8000/about
http://127.0.0.1:8000/users
```

### 💻 `curl`

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/about
curl http://127.0.0.1:8000/users
```

### 🎨 Swagger UI

Visit <http://127.0.0.1:8000/docs> and you will see all three endpoints automatically documented with their response schemas.

---

## 📐 HTTP & Routing Concepts

| Concept | What It Means Here |
|:--------|:-------------------|
| 🌍 **HTTP Method** | We use only `GET` here — data is *read*, never modified. |
| 🛣️ **Path / Route** | Each `@app.get("/xyz")` registers a URL path. |
| ⚙️ **Handler function** | The `def` immediately under the decorator runs when the path matches. |
| 📤 **Return value** | A Python `dict` or `list` — FastAPI converts it to JSON. |
| ✅ **Status code** | `200 OK` is the default for successful `GET`. |

---

## ⚠️ Common Pitfalls

| 😖 Pitfall | ✅ Fix |
|:-----------|:------|
| 🏷️ **Duplicate handler names** — both `/about` and `/users` are named `about`. | Rename them — unique names avoid confusion. |
| 🔁 **Forgot to restart Uvicorn** | Without `--reload`, manual edits will not take effect. |
| 🔀 **Trailing slash mismatch** — `/about` vs `/about/`. | Use the URL FastAPI documents in `/docs`. |
| 📦 **Hard-coded data** | Fine for learning; real apps read from a database. |

---

## 🔧 Suggested Refactor

A cleaner version of this file would be:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to fastapi"}

@app.get("/about")
def about_page():
    return {"message": "This is about page"}

@app.get("/users")
def list_users():
    return {"users": ["Adnan", "umar", "Md"]}
```

---

## 🚀 Where to Go Next

| Next Module | Topic |
|:------------|:------|
| ⬅️ [`A002`](../A002_FastAPI_Tutorial/) | Hello World |
| ➡️ [`A004`](../A004_Path_Parameter_Dynamic_Route_Validation/) | Path parameters and validation |
| ➡️ [`A005`](../A005_Query_Parameters_Optional_Default_Value/) | Optional query parameters |
| ➡️ [`A001`](../A001_CrashCourse/) | Full CRUD with Pydantic |

---

<div align="center">

### 🛣️ *Three routes down — dynamic routes coming up in A004!* 🛣️

Made with ❤️ for FastAPI learners.

</div>