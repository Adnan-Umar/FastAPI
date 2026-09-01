<div align="center">

# 🎯 A004 — Path Parameters & Dynamic Route Validation

### *Capture the URL. Validate automatically. Document for free.*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Difficulty](https://img.shields.io/badge/Level-Beginner+-yellow?style=for-the-badge)
![Reading Time](https://img.shields.io/badge/Read_Time-30_min-blueviolet?style=for-the-badge)
![Auto-Validation](https://img.shields.io/badge/Auto--Validation-✅-success?style=for-the-badge)

</div>

---

## 🧠 The One-Sentence Summary

> **Anything inside `{...}` in a route is captured into a variable, and the function's type hint decides what counts as valid.**

That sentence alone is worth 80% of this README.

---

## 📑 Table of Contents

- [🧠 The One-Sentence Summary](#-the-one-sentence-summary)
- [📖 The 30-Second Story](#-the-30-second-story)
- [🎯 What You Will Learn (8 Skills)](#-what-you-will-learn-8-skills)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧠 Anatomy of `main.py` — Line by Line](#-anatomy-of-mainpy--line-by-line)
- [🛣️ API Endpoints](#-api-endpoints)
- [🔍 Key Concepts (8 of Them)](#-key-concepts-8-of-them)
- [🧪 Try It](#-try-it)
- [⚠️ Common Pitfalls & Fixes](#-common-pitfalls--fixes)
- [🔧 Suggested Extensions](#-suggested-extensions)
- [🧠 Mnemonic Cheat Sheet](#-mnemonic-cheat-sheet)
- [🧪 Recall Test](#-recall-test)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 📖 The 30-Second Story

Old way: parse URL strings with regex, manually cast `int(user_id)`, write try/except, return custom error messages. **40 lines.**

FastAPI way: declare `{user_id}` in the path, type-hint `int` in the function. **2 lines.** FastAPI does the rest.

---

## 🎯 What You Will Learn (8 Skills)

| # | 🎯 Skill | 🧠 You'll remember it because... |
|:-:|:---------|:--------------------------------|
| 1 | 🛣️ `{var}` syntax in path | "Curly braces = capture slot" |
| 2 | 🆔 Variable becomes parameter | "The name in `{...}` matches the function arg" |
| 3 | 💡 Type hint drives validation | "`int` = numeric only" |
| 4 | ❌ 422 on bad type | "Restaurant reservation analogy" |
| 5 | 🔄 Auto type coercion | `"42"` → `42` automatically |
| 6 | 📚 Swagger UI shows type | "Visit `/docs`, see the integer" |
| 7 | 🧰 `Path()` for constraints | "Add rules: `ge=1, le=10000`" |
| 8 | 🔀 Order of routes matters | "Specific before catch-all" |

---

## 📂 Project Structure

```
📁 A004_Path_Parameter_Dynamic_Route_Validation/
├── 🐍 main.py     ← single dynamic route
└── 📖 README.md   ← you are here
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

---

## 🧠 Anatomy of `main.py` — Line by Line

```python
from fastapi import FastAPI

app = FastAPI()

#Users route
@app.get("/users/{user_id}")
def getUserFromId(user_id: int):
    return {"user_id": user_id}
```

| Line | Code | 🧠 Why it's there |
|:----:|:-----|:------------------|
| 1 | `from fastapi import FastAPI` | Framework import |
| 3 | `app = FastAPI()` | Single ASGI instance |
| 6 | `@app.get("/users/{user_id}")` | The **{user_id}** is a path variable |
| 7 | `def getUserFromId(user_id: int)` | `user_id: int` — the **type hint is the validator** |
| 8 | `return {"user_id": user_id}` | Echoes back the (already validated) integer |

---

## 🛣️ API Endpoints

| Method | Endpoint | Description | Example URL |
|:------:|:---------|:------------|:------------|
| 🟢 GET | `/users/{user_id}` | Returns the validated user id | `/users/42` |

### ✅ Success Examples

| Request | Response |
|:--------|:---------|
| `GET /users/1` | `{ "user_id": 1 }` |
| `GET /users/99` | `{ "user_id": 99 }` |
| `GET /users/1234567` | `{ "user_id": 1234567 }` |

### ❌ Validation Failure Example

```bash
GET /users/abc
```

```json
HTTP 422 Unprocessable Entity
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

> 🧠 **Mnemonic: "422 = 'I can't cook this'"** — the chef (your function) never even hears about it.

---

## 🔍 Key Concepts (8 of Them)

### 1️⃣ The `{name}` Syntax

```python
@app.get("/users/{user_id}")
```

`{user_id}` is a *capture slot*. Whatever text fills that slot in the request becomes the value passed as the `user_id` argument.

> 🧠 **Metaphor:** `{user_id}` is a **form field on the URL**. The user fills it in.

### 2️⃣ Type Hint = Validator

```python
def get_user(user_id: int): ...
```

The `int` hint is the contract:

| URL segment | Hint | Behavior |
|:------------|:-----|:---------|
| `"42"` | `int` | ✅ Converted to `42` |
| `"-5"` | `int` | ✅ Converted to `-5` |
| `"abc"` | `int` | ❌ 422 error |
| `"3.14"` | `int` | ❌ 422 error (not an integer) |
| `""` | `int` | ❌ 422 error |
| `"42"` | `str` | ✅ String `"42"` |
| `"42"` | `float` | ✅ Float `42.0` |
| `"42"` | `Path(..., ge=1)` | ❌ 422 if less than 1 |

### 3️⃣ Type Coercion Magic

```python
GET /users/42
```

URL is *always* a string. But your function receives `int`. FastAPI coerced it.

> 🧠 **Metaphor:** Like a translator at the UN — the URL spoke "string", your function speaks "integer", FastAPI translates.

### 4️⃣ Validation Happens BEFORE the Function

```
Request  →  FastAPI  →  Type hint check  →  ✅ Pass  →  Your function
                                  ↓
                              ❌ Fail  →  422 error
```

Your function **never runs** with bad input. That's the magic.

### 5️⃣ Editor Superpowers

Because of the type hint, VS Code / PyCharm know:
- `user_id` is an `int`
- You can do `user_id + 1`, `len(str(user_id))`, etc.
- Autocomplete works perfectly

### 6️⃣ The 422 Response Shape

Every validation error from FastAPI looks like:

```json
{
  "detail": [
    {
      "type": "int_parsing",       ← what kind of error
      "loc": ["path", "user_id"],  ← where in the request
      "msg": "...",                ← human message
      "input": "abc"               ← what you sent
    }
  ]
}
```

> 🧠 **Mnemonic:** "**TLMI**" — **T**ype, **L**ocation, **M**essage, **I**nput.

### 7️⃣ Path() for Constraints

```python
from fastapi import Path

@app.get("/users/{user_id}")
def get_user(user_id: int = Path(..., ge=1, le=10_000)):
    return {"user_id": user_id}
```

| Argument | Meaning | Example |
|:---------|:--------|:--------|
| `...` | Required (Ellipsis) | Always used in `Path(...)` |
| `ge=1` | Greater than or equal | 0 fails, 1 passes |
| `le=10000` | Less than or equal | 10001 fails |
| `min_length` | String min length | For `str` params |
| `max_length` | String max length | For `str` params |
| `regex` | Match pattern | `regex="^a"` |

### 8️⃣ Path vs Query Parameters

| Feature | Path Parameter | Query Parameter |
|:--------|:---------------|:----------------|
| Position | In the URL path | After `?` |
| Required? | By default yes | By default no |
| Example URL | `/users/42` | `/users?id=42` |
| Declaration | `/users/{user_id}` | `def fn(user_id: int = 0)` |

> 🧠 **Mnemonic: "Path = Required, Query = Optional"** — like a passport vs a ticket.

---

## 🧪 Try It

```bash
# ✅ Valid integer
curl http://127.0.0.1:8000/users/42

# ✅ Negative integer (still valid by default)
curl http://127.0.0.1:8000/users/-1

# ❌ Non-integer — see the magic 422
curl http://127.0.0.1:8000/users/abc
```

---

## ⚠️ Common Pitfalls & Fixes

| 😖 Pitfall | 🔍 Cause | ✅ Fix |
|:-----------|:---------|:------|
| `user_id` is a string in your function | You forgot the `int` hint | Add `user_id: int` |
| `/users/42.5` returns 422 | Type hint is `int` | Change to `user_id: float` if you want decimals |
| `/users/me` doesn't work | `/users/{user_id}` captures it as `me` and 422s | Register `/users/me` *before* the dynamic route |
| Need to reject negative IDs | Default accepts them | Use `Path(..., ge=1)` |
| Empty `/users/` matches something | It doesn't — FastAPI's `[^/]+` regex requires at least one char | That's correct behavior |

### 🧠 The Ordering Rule

```python
# ✅ Correct order
@app.get("/users/me")          # specific first
def read_me(): ...

@app.get("/users/{user_id}")   # catch-all second
def read_user(user_id: int): ...
```

> 🧠 **Mnemonic:** "**Specific before General**" — emergency numbers go before the auto-attendant.

---

## 🔧 Suggested Extensions

### 1️⃣ Constrained integer

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int = Path(..., title="The ID", ge=1)):
    return {"user_id": user_id, "valid": True}
```

### 2️⃣ UUID path parameter

```python
from uuid import UUID

@app.get("/orders/{order_id}")
def get_order(order_id: UUID):
    return {"order_id": str(order_id)}
```

### 3️⃣ Multiple path parameters

```python
@app.get("/users/{user_id}/orders/{order_id}")
def get_user_order(user_id: int, order_id: int):
    return {"user_id": user_id, "order_id": order_id}
```

---

## 🧠 Mnemonic Cheat Sheet

| Concept | Mnemonic | Story |
|:--------|:---------|:------|
| `{name}` syntax | "Curly braces = capture slot" | Form fields on the URL |
| `int` hint = validator | "Type = bouncer" | Only numbers past the velvet rope |
| 422 error | "I can't cook this" | Chef never hears about bad orders |
| Error response | "TLMI" | Type, Location, Message, Input |
| Constraint args | "ge le min max" | Greater/less, min/max length |
| Route order | "Specific before General" | Emergency lines before auto-attendant |

---

## 🧪 Recall Test

1. What does `{user_id}` do in a path?
2. Why is `int` better than `str` for an id parameter?
3. What status code does FastAPI return for `/users/abc`?
4. What's in the `loc` field of a 422 error?
5. Which route gets matched first: `/users/me` or `/users/{user_id}`?
6. What does `ge=1` mean in `Path(..., ge=1)`?

> 6/6 → path params are yours forever.

---

## 🚀 Where to Go Next

| Direction | Module |
|:----------|:-------|
| ⬅️ Previous | [A003](../A003_Built_First_FastAPI/) |
| ➡️ Next | [A005](../A005_Query_Parameters_Optional_Default_Value/) — Query params |
| ⬅️ Back | [Root README](../README.md) |

---

<div align="center">

### 🎯 *Captured. Validated. Documented. For free.* 🎯

Made with ❤️ and a pair of curly braces.

---

## 🎯 Interview Q&A

### Q1: What is a path parameter?

**Answer:** A **path parameter** is a variable part of the URL path itself, declared with `{name}` in the route and captured into a function argument by the same name.

```python
@app.get("/users/{user_id}")
def get_user(user_id: int): ...    # user_id captured from URL
```

> **One-liner:** *"`{name}` in the path = variable in the function."*

### Q2: How does FastAPI validate path parameters?

**Answer:** Via the **Python type hint** on the function argument. The hint tells FastAPI to:

- ✅ Try to convert the URL string to that type
- ❌ Return 422 if conversion fails

```python
def get_user(user_id: int): ...    # "abc" → 422, "42" → 42
```

> **One-liner:** *"Type hint = validator. The type does the work."*

### Q3: How do you add constraints like minimum/maximum to a path parameter?

**Answer:** Use `Path()` from FastAPI:

```python
from fastapi import Path

@app.get("/users/{user_id}")
def get_user(user_id: int = Path(..., ge=1, le=10_000)):
    ...
```

`ge` = greater or equal, `le` = less or equal, `gt`, `lt` for strict. The `...` means "required".

> **One-liner:** *"`Path(..., ge=1, le=N)` adds numeric constraints."*

### Q4: Why is route registration order important for path parameters?

**Answer:** FastAPI matches routes **top-down**. Static routes must be registered **before** dynamic catch-alls:

```python
@app.get("/users/me")          # specific
@app.get("/users/{user_id}")   # catch-all
```

Otherwise `/users/me` would match `{user_id}` and become a 422.

> **One-liner:** *"Specific before general — top-down matching."*

### Q5: How can you make a path parameter accept a UUID instead of an int?

**Answer:** Use the `UUID` type from the standard library:

```python
from uuid import UUID

@app.get("/orders/{order_id}")
def get_order(order_id: UUID): ...
```

FastAPI parses and validates the UUID; invalid UUIDs return 422.

> **One-liner:** *"Type-hint with `UUID` and FastAPI parses it for you."*

### Q6: What's the difference between path and query parameters?

**Answer:**

| Path | Query |
|:-----|:------|
| Inside URL path | After `?` |
| Required (by default) | Optional (by default) |
| `/users/42` | `/users?id=42` |
| Identifies a resource | Filters / paginates |

> **One-liner:** *"Path = identity. Query = filter."*

### Q7: How does FastAPI return validation errors for path params?

**Answer:** A **`422 Unprocessable Entity`** with a structured body:

```json
{
  "detail": [{
    "type": "int_parsing",
    "loc": ["path", "user_id"],
    "msg": "Input should be a valid integer...",
    "input": "abc"
  }]
}
```

The `loc` array tells you exactly which field failed.

> **One-liner:** *"422 with TLMI shape (Type, Location, Message, Input)."*

### Q8: Can a path parameter be optional? How?

**Answer:** Path parameters are **required by default** (otherwise the route wouldn't match). To make one optional, declare a *separate* route with a different path:

```python
@app.get("/users/{user_id}")  # /users/42
def get_user(user_id: int): ...

@app.get("/users/")           # /users (no id)
def list_users(): ...
```

> **One-liner:** *"Path params can't be optional. Make a sibling route instead."*

</div>