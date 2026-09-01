<div align="center">

# 🎯 A004 — Path Parameters & Dynamic Route Validation

### *Capture, validate, and document URL segments*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Difficulty](https://img.shields.io/badge/Level-Beginner+-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-blue?style=for-the-badge)
![Validation](https://img.shields.io/badge/Auto--Validation-✅-success?style=for-the-badge)

<br/>

> Path parameters are values captured from the URL itself. FastAPI uses Python **type hints** to automatically validate, convert, and document them — returning a clean `422 Unprocessable Entity` when validation fails.

</div>

---

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    🎯  /users/{user_id}                                       ║
║                                                               ║
║    Valid:   /users/42    → {"user_id": 42}                    ║
║    Invalid: /users/abc   → 422 Unprocessable Entity           ║
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
- [🔍 Key Concepts](#-key-concepts)
- [🧪 Try It](#-try-it)
- [⚠️ Common Pitfalls](#-common-pitfalls)
- [🔧 Suggested Extensions](#-suggested-extensions)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 🎯 What You Will Learn

| # | Skill | Description |
|:-:|:------|:------------|
| 1 | 🛣️ **Path Parameter** | Capture values from the URL with `{user_id}`. |
| 2 | 💡 **Type-Driven Validation** | The Python hint `int` forces validation. |
| 3 | ❌ **422 Errors** | See what happens for non-numeric input. |
| 4 | 📤 **Echo in JSON** | The captured value is returned as JSON. |
| 5 | 🎨 **Swagger UI** | The dynamic segment appears as a placeholder. |
| 6 | 🧰 **Path() Helper** | Add metadata and constraints. |

---

## 📂 Project Structure

```
📁 A004_Path_Parameter_Dynamic_Route_Validation/
├── 🐍 main.py     # Single dynamic route
└── 📖 README.md   # You are here
```

---

## ⚙️ Installation & Setup

```powershell
cd D:\AllProgram\LEARN\Python\FastAPI\A004_Path_Parameter_Dynamic_Route_Validation
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "fastapi[standard]"
uvicorn main:app --reload
```

Visit <http://127.0.0.1:8000/docs>.

---

## 🧠 Anatomy of `main.py`

```python
from fastapi import FastAPI

app = FastAPI()

#Users route
@app.get("/users/{user_id}")
def getUserFromId(user_id: int):
    return {"user_id": user_id}
```

### 🔍 Line-by-Line Breakdown

| Line | Code | Explanation |
|:----:|:-----|:------------|
| 1 | `from fastapi import FastAPI` | Framework import. |
| 3 | `app = FastAPI()` | Application instance. |
| 6 | `@app.get("/users/{user_id}")` | Registers a route where `{user_id}` is a **path variable** — anything in that URL slot is captured. |
| 7 | `def getUserFromId(user_id: int)` | The captured value is passed to the handler. The `int` annotation **forces type validation**. |
| 8 | `return {"user_id": user_id}` | Echoes the validated value back as JSON. |

---

## 🛣️ API Endpoints

| Method | Endpoint | Description | Example URL |
|:------:|:---------|:------------|:------------|
| 🟢 **GET** | `/users/{user_id}` | Returns the validated user id from the URL. | `/users/42` |

### ✅ Successful Calls

| Request | Response |
|:--------|:---------|
| `GET /users/1` | `{ "user_id": 1 }` |
| `GET /users/99` | `{ "user_id": 99 }` |
| `GET /users/1234567` | `{ "user_id": 1234567 }` |

### ❌ Validation in Action — Invalid Call

```bash
GET /users/abc
```

FastAPI responds with HTTP **422 Unprocessable Entity**:

```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["path", "user_id"],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "abc"
    }
  ]
}
```

The framework **never reaches** your handler — validation happens *before* the function is called.

---

## 🔍 Key Concepts

### 1️⃣ Path vs Query Parameters

| Feature | Path Parameter | Query Parameter |
|:--------|:---------------|:----------------|
| 📍 **Position** | Inside the URL path | After `?` in the URL |
| ❗ **Required?** | Usually yes | Optional by default |
| 🌐 **Example URL** | `/users/42` | `/users?id=42` |
| ✍️ **How to declare** | `/users/{user_id}` | `def get_user(user_id: int = 0)` |

### 2️⃣ Type-Hint-Driven Validation

The hint `user_id: int` triggers a stack of automatic behaviour:

| Behaviour | Benefit |
|:----------|:--------|
| 🔄 **Type conversion** | `"42"` → `42` |
| 🛡️ **Validation** | Rejects `"abc"`, `""`, `"3.14"`, etc. |
| 📚 **Documentation** | Swagger UI shows the type as `integer`. |
| 🧠 **Editor support** | VS Code / PyCharm autocomplete inside the handler. |

### 3️⃣ Path Validation Rules

FastAPI uses the standard library regex `[^/]+` to capture the segment. For stricter rules use `Path`:

```python
from fastapi import Path

@app.get("/users/{user_id}")
def get_user(user_id: int = Path(..., ge=1, le=10_000)):
    return {"user_id": user_id}
```

This rejects negative numbers, zero, or IDs larger than 10 000.

---

## 🧪 Try It

```bash
# ✅ Valid integer id
curl http://127.0.0.1:8000/users/42

# ✅ Negative id (still int, accepted by default)
curl http://127.0.0.1:8000/users/-1

# ❌ Non-integer — 422 error
curl http://127.0.0.1:8000/users/abc
```

---

## ⚠️ Common Pitfalls

| 😖 Pitfall | ✅ Fix |
|:-----------|:------|
| 📦 Handler receives value as a **string** | Add `int` (or `float`, `UUID`, etc.) to the parameter hint. |
| 🧰 Need extra constraints (min/max length, regex) | Use `from fastapi import Path` with `ge`, `le`, `min_length`. |
| 🔀 Order matters when mixing `/users/me` and `/users/{user_id}` | Define **fixed paths first** — `/users/me` must be registered *before* `/users/{user_id}`. |
| 🔁 Forgetting `--reload` after edits | Restart Uvicorn manually. |

### 🔀 Route-Ordering Example

```python
@app.get("/users/me")        # registered first
def read_me():
    return {"user_id": "me"}

@app.get("/users/{user_id}") # catch-all, registered second
def read_user(user_id: int):
    return {"user_id": user_id}
```

`/users/me` returns the static handler; `/users/42` falls through to the dynamic one.

---

## 🔧 Suggested Extensions

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(
    user_id: int = Path(..., title="The ID of the user", ge=1)
):
    return {"user_id": user_id, "valid": True}
```

You now have **metadata, validation, and docs** all from one parameter declaration.

---

## 🚀 Where to Go Next

| Next Module | Topic |
|:------------|:------|
| ⬅️ [`A003`](../A003_Built_First_FastAPI/) | Multi-Route App |
| ➡️ [`A005`](../A005_Query_Parameters_Optional_Default_Value/) | Optional query parameters |
| ⬅️ [`A001`](../A001_CrashCourse/) | Full CRUD with Pydantic |
| 🌐 Official docs | <https://fastapi.tiangolo.com/tutorial/path-params/> |

---

<div align="center">

### 🎯 *You've captured URL segments — now learn to filter with query strings in A005!* 🎯

Made with ❤️ for FastAPI learners.

</div>