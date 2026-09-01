<div align="center">

# 🔌 A013 — Dependency Injection: `Depends()` & Auth Example

### *Stop copy-pasting the same logic into every route. Inject it.*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![DI](https://img.shields.io/badge/Dependency_Injection-🔌-blueviolet?style=for-the-badge)
![Auth](https://img.shields.io/badge/Auth-🔐-red?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Level-Advanced-red?style=for-the-badge)
![Reading Time](https://img.shields.io/badge/Read_Time-50_min-blueviolet?style=for-the-badge)

</div>

---

## 🧠 The One-Sentence Summary

> **`Depends(some_function)` runs `some_function` *before* your endpoint and passes its return value in — like a function call that FastAPI wires up for you.**

If you remember *"Depends = 'call this first, give me the result'"*, the rest of this README is decoration.

---

## 📑 Table of Contents

- [🧠 The One-Sentence Summary](#-the-one-sentence-summary)
- [📖 The Story: The Restaurant Kitchen Brigade](#-the-story-the-restaurant-kitchen-brigade)
- [🎯 What You Will Learn (12 Skills)](#-what-you-will-learn-12-skills)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧬 Anatomy of `main.py` — Line by Line](#-anatomy-of-mainpy--line-by-line)
- [🛣️ API Endpoints](#-api-endpoints)
- [🧠 The Mental Model: What DI Actually Does](#-the-mental-model-what-di-actually-does)
- [🔬 Deep Dive: The `verify_token` Dependency](#-deep-dive-the-verify_token-dependency)
- [🔬 Deep Dive: `Depends()` Mechanics](#-deep-dive-dependends-mechanics)
- [🪜 The Three Levels of Dependencies (Mnemonic: **S-C-D**)](#-the-three-levels-of-dependencies-mnemonic-s-c-d)
- [🧪 Try It With curl](#-try-it-with-curl)
- [🔧 Variations You Should Know](#-variations-you-should-know)
- [⚠️ Common Pitfalls & Fixes](#-common-pitfalls--fixes)
- [🧠 Mnemonic Cheat Sheet](#-mnemonic-cheat-sheet)
- [🧪 Recall Test](#-recall-test)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 📖 The Story: The Restaurant Kitchen Brigade

Imagine a busy restaurant kitchen 🍳. Every chef is a *route*. Before any dish is cooked, the same prep work happens:

1. 🥬 Wash the vegetables
2. 🔪 Chop them
3. 🧂 Measure the spices

**Old way:** Every chef washes, chops, measures — duplicated 30 times.

**New way:** There's a **prep cook** standing at the door. Every chef gets the prep work handed to them, ready to cook. That's **`Depends()`**.

The prep cook is the **dependency**. The chef is your **route function**. The dish is the **response**.

> 🧠 **Mnemonic:** "**Depends = prep cook**" — they do the work before you do.

---

## 🎯 What You Will Learn (12 Skills)

| # | 🎯 Skill | 🧠 You'll remember it because... |
|:-:|:---------|:--------------------------------|
| 1 | 🔌 **What `Depends()` does** | "Runs first, hands you the result" |
| 2 | 📦 **Define a dependency** | "Just a function" |
| 3 | 🎯 **Inject a dependency** | "`param = Depends(func)`" |
| 4 | 🔐 **Auth with `Header`** | "Read a custom header" |
| 5 | 🚨 **Reject in dependency** | "Raise HTTPException, request never reaches you" |
| 6 | 🔁 **Reuse across routes** | "One function, many endpoints" |
| 7 | 🪜 **Nested dependencies** | "Depends that depend on other Depends" |
| 8 | 🏛️ **Class-based dependencies** | "Use a class with `__init__` for config" |
| 9 | 🎁 **Yield dependencies** | "Setup + teardown (DB sessions!)" |
| 10 | 🛡️ **Use `use_cache`** | "Cache the result per request" |
| 11 | 📤 **Override in tests** | "Replace with a fake during testing" |
| 12 | 🧠 **Why DI matters** | "DRY + testable + composable" |

---

## 📂 Project Structure

```
📁 A013_Dependency_Injection_Depends()_Auth_Example/
├── 🐍 main.py     ← 46 lines: active auth + 3 commented progressions
└── 📖 README.md   ← you are here
```

---

## ⚙️ Installation & Setup

```powershell
cd D:\AllProgram\LEARN\Python\FastAPI\A013_Dependency_Injection_Depends()_Auth_Example
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "fastapi[standard]"
uvicorn main:app --reload
```

Visit <http://127.0.0.1:8000/docs> — try the `/secure-data` endpoint **without** and **with** the `token` header.

---

## 🧬 Anatomy of `main.py` — Line by Line

```python
from fastapi import FastAPI, Depends, Header, HTTPException

app = FastAPI()

# The dependency — runs BEFORE the route
def verify_token(token: str = Header(None)):
    if token != "mysecrettoken":
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    return {
        "user": "Authorized user"
    }

# The route — receives the dependency's return value
@app.get("/secure-data")
def secure_data(user = Depends(verify_token)):
    return {
        "message": "Secured data accessed",
        "user": user
    }
```

| Lines | Code | 🧠 Why it's there |
|:-----:|:-----|:------------------|
| 1 | Imports | FastAPI + `Depends` + `Header` + `HTTPException` |
| 3 | `app = FastAPI()` | App instance |
| 5–13 | `verify_token` | **Dependency** — checks `token` header, raises 401 if bad |
| 15–20 | `@app.get("/secure-data")` + `Depends(verify_token)` | **Route** — only runs if dependency passes |

### The Three Magic Lines

```python
def verify_token(token: str = Header(None)):    # 1. The dependency
    ...

@app.get("/secure-data")
def secure_data(user = Depends(verify_token)):  # 2. The injection
    ...                                          # 3. Your code uses `user`
```

> 🧠 **Mnemonic:** "**D-I-U**" — **D**efine, **I**nject, **U**se.

### 🎯 If you remember ONE thing
> **A dependency is just a function. `Depends(func)` makes FastAPI call it for you and hand you the return value.**

---

## 🛣️ API Endpoints

| Method | Endpoint | Auth Required? | Behavior |
|:------:|:---------|:---------------|:---------|
| 🟢 GET | `/secure-data` | ✅ Yes (`token` header) | Returns data if token is valid, else `401` |

---

## 🧠 The Mental Model: What DI Actually Does

Without DI (the old way):

```python
def secure_data(token: str = Header(None)):
    if token != "mysecrettoken":
        raise HTTPException(401, "Unauthorized")
    return {"data": "secret"}
```

With DI (the new way):

```python
def verify_token(token: str = Header(None)):
    if token != "mysecrettoken":
        raise HTTPException(401, "Unauthorized")
    return {"user": "Authorized user"}

def secure_data(user = Depends(verify_token)):
    return {"data": "secret", "user": user}
```

### What's the Real Difference?

| Aspect | Old way | DI way |
|:-------|:--------|:-------|
| Logic in every route | ❌ Duplicated | ✅ Single function |
| Easy to reuse | ❌ No | ✅ Yes — `Depends(verify_token)` anywhere |
| Easy to test | ❌ Hard (auth mixed in) | ✅ Easy (replace the dep) |
| Easy to change | ❌ Touch every route | ✅ Touch one function |

> 🧠 **Mnemonic:** "**DRY + Test + Composable**" — the three gifts of DI.

---

## 🔬 Deep Dive: The `verify_token` Dependency

### Anatomy

```python
def verify_token(token: str = Header(None)):
    if token != "mysecrettoken":
        raise HTTPException(401, "Unauthorized")
    return {"user": "Authorized user"}
```

| Piece | What it does |
|:------|:-------------|
| `token: str = Header(None)` | Pulls `token` from request headers, default `None` if missing |
| `if token != "mysecrettoken"` | Validates the token (real-world: check DB, JWT, etc.) |
| `raise HTTPException(401, ...)` | **Rejects** the request — your route never runs |
| `return {...}` | **Passes data** to the route |

### The `Header(None)` Magic

`Header(None)` tells FastAPI:

> "Look for a header named `token` (case-insensitive). If absent, use `None`."

So the actual HTTP request must be:

```http
GET /secure-data HTTP/1.1
Host: 127.0.0.1:8000
token: mysecrettoken       ← this is what Header(None) reads
```

> 🧠 **Mnemonic:** "**Header = from headers, Query = from `?`, Body = from JSON**."

### What Happens If Token Is Missing?

```bash
curl http://127.0.0.1:8000/secure-data
```

1. `verify_token` is called with `token=None`
2. `None != "mysecrettoken"` → `True`
3. Raises `HTTPException(401, "Unauthorized")`
4. Your route's body never executes
5. Client gets `401`

---

## 🔬 Deep Dive: `Depends()` Mechanics

### How It Looks vs What Happens

```python
def secure_data(user = Depends(verify_token)):
    return {"user": user}
```

FastAPI internally rewrites this as:

```python
def secure_data():
    # Run verify_token first
    user = verify_token()
    return {"user": user}
```

That's it. `Depends` is **syntactic sugar** for "call this first, bind the result to this name".

> 🧠 **Mnemonic:** "**Depends = automatic function call**."

### What `Depends` Returns

Whatever the dependency function returns. In this case: `{"user": "Authorized user"}`.

### You Can Use It in Any Parameter Position

```python
def endpoint(
    user = Depends(verify_token),     # 1st
    db = Depends(get_db),              # 2nd
    settings = Depends(get_settings)   # 3rd
):
    ...
```

FastAPI runs them in order and binds each result.

---

## 🪜 The Three Levels of Dependencies (Mnemonic: **S-C-D**)

| Level | Type | Example | Use case |
|:------|:-----|:--------|:---------|
| 🟢 **Simple** | Plain function | `verify_token` | Auth, validation |
| 🟡 **Class** | Class with `__init__` | Settings, config | Reusable config |
| 🔴 **Yield** | Function with `yield` | DB sessions, transactions | Setup + teardown |

> 🧠 **Mnemonic:** "**S-C-D**" → **S**imple, **C**lass, **D**atabase-style (yield). Increasing power, increasing complexity.

### Level 1 — Simple Function (in this module)

```python
def verify_token(token: str = Header(None)):
    if token != "mysecrettoken":
        raise HTTPException(401, "Unauthorized")
    return {"user": "Authorized user"}
```

### Level 2 — Class-based

```python
class QueryParams:
    def __init__(self, skip: int = 0, limit: int = Query(10, le=100)):
        self.skip = skip
        self.limit = limit

@app.get("/items")
def list_items(params: QueryParams = Depends()):
    return {"skip": params.skip, "limit": params.limit}
```

> 🧠 **Mnemonic:** "**Class-based = reusable config object**."

### Level 3 — Yield (the killer feature)

```python
def get_db():
    db = SessionLocal()
    try:
        yield db                # ← route runs here
    finally:
        db.close()              # ← always runs after
```

FastAPI handles the cleanup automatically. **This is how DB sessions are done in FastAPI.**

> 🧠 **Mnemonic:** "**Yield = setup + teardown**."

---

## 🧪 Try It With curl

### ✅ With valid token

```bash
curl -H "token: mysecrettoken" http://127.0.0.1:8000/secure-data
```

```json
{
  "message": "Secured data accessed",
  "user": {"user": "Authorized user"}
}
```

### ❌ Without token

```bash
curl -i http://127.0.0.1:8000/secure-data
```

```http
HTTP/1.1 422 Unprocessable Entity
```

Why 422? Because `Header(None)` doesn't accept a missing header gracefully. To make it return 401 instead, use a different approach:

```python
from fastapi import Header
from typing import Optional

def verify_token(token: Optional[str] = Header(None, alias="token")):
    if token is None:
        raise HTTPException(401, "Token header missing")
    if token != "mysecrettoken":
        raise HTTPException(401, "Invalid token")
    return {"user": "Authorized user"}
```

### ❌ With wrong token

```bash
curl -i -H "token: wrongtoken" http://127.0.0.1:8000/secure-data
```

```http
HTTP/1.1 401 Unauthorized
content-type: application/json
{"detail": "Unauthorized"}
```

---

## 🔧 Variations You Should Know

### 1️⃣ Reuse one dependency across many routes

```python
def verify_token(token: str = Header(None)):
    ...

@app.get("/secure-data")
def secure_data(user = Depends(verify_token)):
    ...

@app.get("/profile")
def profile(user = Depends(verify_token)):
    return user

@app.get("/dashboard")
def dashboard(user = Depends(verify_token)):
    return user
```

Same auth check, three routes. **DRY** ✓

### 2️⃣ Dependencies of dependencies

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db = Depends(get_db), token: str = Header(None)):
    user = db.query(User).filter_by(token=token).first()
    if not user:
        raise HTTPException(401, "Invalid token")
    return user

@app.get("/profile")
def profile(user = Depends(get_current_user)):    # ← depends on Depends(get_db)
    return user
```

> 🧠 **Mnemonic:** "**Depends all the way down**" — like Russian dolls.

### 3️⃣ Return a Pydantic model from dependency

```python
class CurrentUser(BaseModel):
    id: int
    name: str

def get_current_user() -> CurrentUser:
    return CurrentUser(id=1, name="Adnan")

@app.get("/me")
def me(user: CurrentUser = Depends(get_current_user)):
    return user
```

### 4️⃣ Override in tests

```python
from fastapi.testclient import TestClient

def fake_token():
    return {"user": "Test User"}

app.dependency_overrides[verify_token] = fake_token

client = TestClient(app)
response = client.get("/secure-data")   # uses fake_token
```

### 5️⃣ Cache the result (`use_cache=True`)

```python
def get_settings():
    return load_config()    # expensive

@app.get("/items")
def items(s = Depends(get_settings, use_cache=True)):
    return s
```

`use_cache=True` (default) means FastAPI calls the dependency **once per request**, even if you reference it in multiple places.

> 🧠 **Mnemonic:** "**Cache = call once, hand out many**."

### 6️⃣ Use `Security()` for OpenAPI docs

```python
from fastapi import Security

def verify_token(token: str = Header(None)):
    ...

@app.get("/secure-data")
def secure_data(user = Security(verify_token)):    # ← Security, not Depends
    ...
```

`Security` is a special `Depends` that **shows up in `/docs` with a 🔒 lock icon**.

---

## ⚠️ Common Pitfalls & Fixes

| 😖 Pitfall | 🔍 Cause | ✅ Fix |
|:-----------|:---------|:------|
| Dependency not running | You forgot `Depends(...)` | Add `= Depends(your_func)` |
| 422 instead of 401 for missing token | `Header(None)` returns None, then your check fails later | Use `Header(None, alias="token")` and explicit None check |
| Dependency runs twice | No caching | `use_cache=True` (default) |
| Can't override in tests | Not using `app.dependency_overrides` | Use the dict to replace |
| Header name is wrong | `Header(None)` looks for `token`, not `Token` or `TOKEN` | Headers are case-insensitive but spelling must match |
| `Security` not showing 🔒 in docs | Used `Depends` instead of `Security` | Use `Security(verify_token)` for auth |

---

## 🧠 Mnemonic Cheat Sheet

| Concept | Mnemonic | Story |
|:--------|:---------|:------|
| What is `Depends` | **Prep cook** | Runs before, hands you the result |
| Three lines | **D-I-U** | Define, Inject, Use |
| Three levels | **S-C-D** | Simple, Class, yield-Database |
| Why DI | **DRY + Test + Composable** | Three gifts |
| `Depends` is | **Automatic function call** | Syntactic sugar |
| `Security` vs `Depends` | **Security = 🔒 in docs** | Same execution, different docs |

---

## 🧪 Recall Test

1. What does `Depends(func)` do?
2. What three things does a dependency enable? (DRY, ?, ?)
3. How do you read a custom header in a dependency?
4. Where do you raise an error in a dependency?
5. How do you reuse one auth check across 3 routes?
6. What's the difference between `Depends` and `Security`?
7. How do you replace a dependency in tests?

> 7/7 → dependency injection is yours forever.

---

## 🚀 Where to Go Next

| Direction | Module |
|:----------|:-------|
| ⬅️ Previous | [A012](../A012_Exception_Handling_HTTPException_Global_Error_Handler/) |
| ⬅️ Back | [Root README](../README.md) |
| ➡️ Next | A014 (planned) — Database with SQLAlchemy & Yield Dependencies |
| ➡️ Future | A015 (planned) — Middleware, CORS, Background Tasks |

---

<div align="center">

### 🔌 *Stop duplicating. Start injecting.* 🔌

Made with ❤️, a prep cook called `Depends`, and a token called `mysecrettoken`.

</div>