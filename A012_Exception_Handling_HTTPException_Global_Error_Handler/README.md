<div align="center">

# 🛡️ A012 — Exception Handling: HTTPException & Global Error Handlers

### *Stop scattering try/except everywhere. Centralize your errors.*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Errors](https://img.shields.io/badge/Global_Handler-🛡️-red?style=for-the-badge)
![Custom](https://img.shields.io/badge/Custom_Exceptions-✅-success?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Level-Advanced-red?style=for-the-badge)
![Reading Time](https://img.shields.io/badge/Read_Time-50_min-blueviolet?style=for-the-badge)

</div>

---

## 🧠 The One-Sentence Summary

> **`@app.exception_handler(MyException)` is a single chokepoint where you decide the HTTP response for every place that raises `MyException` — no more try/except in every function.**

If you remember *"exception handler = single chokepoint"*, the rest of this README is decoration.

---

## 📑 Table of Contents

- [🧠 The One-Sentence Summary](#-the-one-sentence-summary)
- [📖 The Story: The 911 Dispatcher](#-the-story-the-911-dispatcher)
- [🎯 What You Will Learn (12 Skills)](#-what-you-will-learn-12-skills)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧬 Anatomy of `main.py` — Line by Line](#-anatomy-of-mainpy--line-by-line)
- [🛣️ API Endpoints](#-api-endpoints)
- [🧠 The Mental Model: The Exception Flow](#-the-mental-model-the-exception-flow)
- [🔬 Deep Dive: Custom Exceptions](#-deep-dive-custom-exceptions)
- [🔬 Deep Dive: Global Exception Handlers](#-deep-dive-global-exception-handlers)
- [🧠 The Three Layers of Error Handling](#-the-three-layers-of-error-handling)
- [🧪 Try It With curl](#-try-it-with-curl)
- [🔧 Variations You Should Know](#-variations-you-should-know)
- [⚠️ Common Pitfalls & Fixes](#-common-pitfalls--fixes)
- [🧠 Mnemonic Cheat Sheet](#-mnemonic-cheat-sheet)
- [🧪 Recall Test](#-recall-test)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 📖 The Story: The 911 Dispatcher

Imagine your application as a city. Things go wrong everywhere — fires 🚒, medical emergencies 🚑, crimes 🚓.

**Old way (A011):** Every building has its own little 911 system. Inconsistent, duplicative.

**New way (A012):** There's a single **911 dispatcher** 🎧. Every call routes through one place. The dispatcher knows:

- 🚒 "Fire?" → send firefighters
- 🚑 "Medical?" → send ambulance
- 🚓 "Crime?" → send police

That's what `@app.exception_handler(...)` does. You raise a custom exception from anywhere in your code, and **one function** decides what HTTP response to send.

> 🧠 **Mnemonic:** "**Exception handler = 911 dispatcher**" — one place to call, consistent responses.

---

## 🎯 What You Will Learn (12 Skills)

| # | 🎯 Skill | 🧠 You'll remember it because... |
|:-:|:---------|:--------------------------------|
| 1 | 🆕 **Custom exception class** | "Inherit from `Exception`" |
| 2 | 🎯 **Raise a custom exception** | "Like raising `HTTPException`" |
| 3 | 🛡️ **`@app.exception_handler(...)`** | "The 911 dispatcher" |
| 4 | 📨 **`Request` parameter** | "Access headers, URL, body if needed" |
| 5 | 📤 **`JSONResponse` return** | "Build the response shape yourself" |
| 6 | 🔍 **Catch the exception type** | "Specific dispatch" |
| 7 | 🌍 **Catch `Exception` (catch-all)** | "Last resort" |
| 8 | 🪜 **Layered handlers** | "Specific before general" |
| 9 | 🆚 **Custom vs `HTTPException`** | "Domain vs generic" |
| 10 | 🛠️ **Reusable error logic** | "Don't repeat yourself" |
| 11 | 📚 **Swagger UI shows 404 response** | "Docs reflect handlers" |
| 12 | 🧠 **Override FastAPI's built-ins** | "Custom 422 handler" |

---

## 📂 Project Structure

```
📁 A012_Exception_Handling_HTTPException_Global_Error_Handler/
├── 🐍 main.py     ← 45 lines: custom exception + global handler
└── 📖 README.md   ← you are here
```

---

## ⚙️ Installation & Setup

```powershell
cd D:\AllProgram\LEARN\Python\FastAPI\A012_Exception_Handling_HTTPException_Global_Error_Handler
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "fastapi[standard]"
uvicorn main:app --reload
```

Visit <http://127.0.0.1:8000/docs> — try `/user/Adnan` (success) and `/user/anything-else` (custom 404).

---

## 🧬 Anatomy of `main.py` — Line by Line

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# 1. Custom exception class
class UserNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name

# 2. Global exception handler — the 911 dispatcher
@app.exception_handler(UserNotFoundException)
def user_not_found_handler(request: Request, exe: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": f"User {exe.name} not found"
        }
    )

# 3. Endpoint that raises the custom exception
@app.get("/user/{name}")
def get_user(name: str):
    if name != "Adnan":
        raise UserNotFoundException(name)
    return {
        "name": name
    }
```

| Lines | Code | 🧠 Why it's there |
|:-----:|:-----|:------------------|
| 1–2 | Imports | FastAPI, `HTTPException`, `Request`, `JSONResponse` |
| 4 | `app = FastAPI()` | App instance |
| 6–9 | `class UserNotFoundException(Exception)` | **Custom domain exception** — carries `name` |
| 11–20 | `@app.exception_handler(UserNotFoundException)` | **911 dispatcher** — what to do when raised |
| 22–30 | `get_user` | The endpoint that raises the custom exception |
| 32–44 | *(commented)* Old `HTTPException` style | A011's approach for comparison |

### 🎯 If you remember ONE thing
> **Define a custom exception class, register a handler with `@app.exception_handler(...)`, raise the exception anywhere — FastAPI routes the response through the handler.**

---

## 🛣️ API Endpoints

| Method | Endpoint | Path Param | Behavior |
|:------:|:---------|:-----------|:---------|
| 🟢 GET | `/user/{name}` | `name: str` | Returns user if name == "Adnan", else `404` via custom handler |

### ✅ Success

```bash
curl http://127.0.0.1:8000/user/Adnan
```

```json
{"name": "Adnan"}
```

### ❌ Custom 404

```bash
curl -i http://127.0.0.1:8000/user/Md
```

```http
HTTP/1.1 404 Not Found
content-type: application/json

{
  "status": "error",
  "message": "User Md not found"
}
```

---

## 🧠 The Mental Model: The Exception Flow

```
┌────────────────────────────────────────────────────────┐
│  Request:  GET /user/Md                                │
│           │                                            │
│           ▼                                            │
│  ┌──────────────────────┐                              │
│  │ get_user()           │                              │
│  │   if name != "Adnan" │                              │
│  │     raise UserNot... │                              │
│  └──────────┬───────────┘                              │
│             │                                          │
│             ▼                                          │
│  ┌──────────────────────────────────────────────┐      │
│  │ FastAPI catches UserNotFoundException         │      │
│  │ Looks up registered handler                  │      │
│  │ Calls: user_not_found_handler(request, exc)  │      │
│  └──────────┬───────────────────────────────────┘      │
│             │                                          │
│             ▼                                          │
│  ┌──────────────────────────────────────┐              │
│  │ JSONResponse(404, {...})             │              │
│  └──────────┬───────────────────────────┘              │
│             │                                          │
│             ▼                                          │
│       Client receives 404 with custom JSON             │
└────────────────────────────────────────────────────────┘
```

> 🧠 **Mnemonic:** "**R-R-H-J-C**" — **R**aise, **R**oute, **H**andler, **J**SONResponse, **C**lient.

---

## 🔬 Deep Dive: Custom Exceptions

### The Anatomy of a Custom Exception

```python
class UserNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name
```

| Piece | What it does |
|:------|:-------------|
| `class UserNotFoundException(Exception)` | Inherit from `Exception` (Python's base) |
| `def __init__(self, name: str)` | Constructor — accepts data |
| `self.name = name` | Store the data on the instance |

When you `raise UserNotFoundException("Md")`, you create an object with `.name = "Md"`. The handler can read that.

### Why Bother with Custom Exceptions?

| Approach | Pros | Cons |
|:---------|:-----|:-----|
| Plain `HTTPException` | Quick, built-in | Limited shape, repeated code |
| Custom exception | Rich payload, central handler | More setup |

> 🧠 **Mnemonic:** "**HTTPException for one-offs, custom for repeats**."

### Multiple Custom Exceptions

```python
class UserNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name

class UserAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email

class InvalidCredentialsException(Exception):
    pass
```

Each can have its own handler with a different status code and shape.

---

## 🔬 Deep Dive: Global Exception Handlers

### The Anatomy

```python
@app.exception_handler(UserNotFoundException)
def user_not_found_handler(request: Request, exe: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": f"User {exe.name} not found"
        }
    )
```

| Piece | What it does |
|:------|:-------------|
| `@app.exception_handler(UserNotFoundException)` | "When this type is raised, call me" |
| `request: Request` | The incoming request (URL, headers, body, method) |
| `exe: UserNotFoundException` | The exception instance — read `.name`, etc. |
| `return JSONResponse(...)` | Build the HTTP response manually |

### What You Can Access via `request`

```python
@app.exception_handler(UserNotFoundException)
def handler(request: Request, exc: UserNotFoundException):
    print(request.url.path)        # /user/Md
    print(request.method)          # GET
    print(request.headers)         # dict of headers
    print(request.query_params)    # query string
    return JSONResponse(404, {"path": str(request.url.path)})
```

### What You Can Return

You can return:

- ✅ `JSONResponse`
- ✅ `Response` (any subclass)
- ✅ `dict` (auto-wrapped as JSON)
- ✅ `PlainTextResponse`
- ✅ A custom `Response` subclass

But **`JSONResponse` is the most common** because it gives you control over `status_code`, `headers`, and `content`.

---

## 🧠 The Three Layers of Error Handling

| Layer | Tool | When | Code |
|:------|:-----|:-----|:----|
| 1️⃣ **Pydantic validation** | Auto | Bad input shape | 422 (built-in) |
| 2️⃣ **Per-route `HTTPException`** | Quick one-off | Single endpoint error | inline `raise HTTPException(...)` |
| 3️⃣ **Custom exception + global handler** | Reusable | Repeated pattern across routes | class + decorator |

> 🧠 **Mnemonic:** "**V-H-G**" — **V**alidation, **H**TTPException, **G**lobal handler. Three layers, in that order.

### Decision Tree

```
Something went wrong. Which layer?
│
├── Wrong input shape (missing field, wrong type)
│   └── Layer 1: Pydantic → 422 (automatic, free)
│
├── Single endpoint, unique error
│   └── Layer 2: HTTPException (A011)
│
└── Repeated pattern (UserNotFound used 5 times)
    └── Layer 3: Custom exception + global handler (A012)
```

---

## 🧪 Try It With curl

```bash
# Success
curl http://127.0.0.1:8000/user/Adnan
# {"name": "Adnan"}

# Custom 404 (via global handler)
curl -i http://127.0.0.1:8000/user/Md
# HTTP/1.1 404 Not Found
# {"status":"error","message":"User Md not found"}

# Special characters in the URL
curl -i "http://127.0.0.1:8000/user/Zara%20Khan"
# {"status":"error","message":"User Zara Khan not found"}
```

### Compare to A011

In A011, raising `HTTPException(404, "User Not Found")` would give:

```json
{"detail": "User Not Found"}
```

In A012, the custom handler gives:

```json
{"status": "error", "message": "User Md not found"}
```

The body is **richer and consistent** across all endpoints that raise the same exception.

---

## 🔧 Variations You Should Know

### 1️⃣ Multiple handlers for different exceptions

```python
@app.exception_handler(UserNotFoundException)
def user_not_found(request, exc):
    return JSONResponse(404, {"error": "user_not_found", "name": exc.name})

@app.exception_handler(ValueError)
def value_error(request, exc):
    return JSONResponse(400, {"error": "value_error", "detail": str(exc)})
```

### 2️⃣ Catch-all handler (last resort)

```python
@app.exception_handler(Exception)
def global_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "internal", "message": "Something went wrong"}
    )
```

> 🧠 **Caution:** Catching `Exception` swallows *everything* including programmer bugs. Use carefully.

### 3️⃣ Override FastAPI's built-in 422

```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def custom_422(request, exc):
    return JSONResponse(
        status_code=422,
        content={"error": "validation", "fields": exc.errors()}
    )
```

### 4️⃣ Access the request body in the handler

```python
@app.exception_handler(UserNotFoundException)
async def handler(request: Request, exc):
    body = await request.json()    # ← async
    return JSONResponse(404, {...})
```

Note: when you `await`, the handler must be `async def`.

### 5️⃣ Add custom headers in the response

```python
@app.exception_handler(UserNotFoundException)
def handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "not_found"},
        headers={"X-Custom-Header": "value"}
    )
```

### 6️⃣ Logging in the handler

```python
import logging

logger = logging.getLogger(__name__)

@app.exception_handler(UserNotFoundException)
def handler(request, exc):
    logger.warning(f"User not found: {exc.name} (path={request.url.path})")
    return JSONResponse(404, {"error": "not_found"})
```

### 7️⃣ Async handler

```python
@app.exception_handler(UserNotFoundException)
async def handler(request: Request, exc: UserNotFoundException):
    # await something if you need to
    return JSONResponse(404, {"error": "not_found"})
```

---

## ⚠️ Common Pitfalls & Fixes

| 😖 Pitfall | 🔍 Cause | ✅ Fix |
|:-----------|:---------|:------|
| Handler not triggered | Wrong exception type | Make sure the raised type matches the registered one |
| `JSONResponse` shows as `null` | Returned `dict` not wrapped | Use `JSONResponse(...)` explicitly |
| `request.json()` hangs | Forgot `await` | Make handler `async def` and `await` the body |
| Catch-all swallows programmer bugs | Catching `Exception` too broadly | Catch specific exceptions first |
| Custom 422 not used | Imported wrong class | Use `RequestValidationError` from `fastapi.exceptions` |
| Swagger UI doesn't show new responses | FastAPI infers from handler — should be fine | Restart Uvicorn if needed |

---

## 🧠 Mnemonic Cheat Sheet

| Concept | Mnemonic | Story |
|:--------|:---------|:------|
| What is a handler | **911 dispatcher** | One place to call |
| Exception flow | **R-R-H-J-C** | Raise, Route, Handler, JSONResponse, Client |
| Three layers | **V-H-G** | Validation, HTTPException, Global handler |
| When to use which | **Repeat = global, one-off = HTTP** | Don't over-engineer |
| Custom exception | **Inherit from Exception** | Python's base |
| Handler return | **JSONResponse for control** | Or dict for simplicity |

---

## 🧪 Recall Test

1. What's the difference between `HTTPException` and a custom exception?
2. What decorator registers a global exception handler?
3. What two parameters does a handler function receive?
4. What's the difference between `def` and `async def` in a handler?
5. How do you return a custom JSON shape from a handler?
6. How do you override FastAPI's built-in 422 handler?
7. What's the risk of catching `Exception` as a catch-all?

> 7/7 → centralized error handling is yours.

---

## 🚀 Where to Go Next

| Direction | Module |
|:----------|:-------|
| ⬅️ Previous | [A011](../A011_Status_Codes_Custom_Responses_Error_Handling/) |
| ⬅️ Back | [Root README](../README.md) |
| ➡️ Next | A013 (planned) — Dependencies & Authentication |
| ➡️ Future | A014 (planned) — Database with SQLAlchemy |

---

<div align="center">

### 🛡️ *Stop scattering try/except. Centralize the chaos.* 🛡️

Made with ❤️, custom exceptions, and a 911 dispatcher called `@app.exception_handler`.

---

## 🎯 Interview Q&A

### Q1: Why use a global exception handler instead of `try/except` in every route?

**Answer:** Centralization. One handler covers all routes that raise the same exception. Less duplication, consistent error shape, easier to change later.

| `try/except` in every route | Global handler |
|:---------------------------|:---------------|
| Duplicated 10+ times | Defined once |
| Inconsistent shapes | One shape |
| Hard to refactor | One place to change |

> **One-liner:** *"Centralize errors. Don't scatter try/except."*

### Q2: How do you create a custom exception in Python?

**Answer:** Subclass `Exception` (or a more specific base):

```python
class UserNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name
```

Raise it like any other:

```python
raise UserNotFoundException("Adnan")
```

> **One-liner:** *"Subclass `Exception`; raise it like any other."*

### Q3: How do you register a global exception handler?

**Answer:** Use `@app.exception_handler(MyException)`:

```python
from fastapi.responses import JSONResponse

@app.exception_handler(UserNotFoundException)
def handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "user_not_found", "name": exc.name}
    )
```

The handler runs whenever that exception is raised anywhere in the app.

> **One-liner:** *"`@app.exception_handler(...)` registers the 911 dispatcher."*

### Q4: What are the two parameters of an exception handler?

**Answer:** `request` and `exc`:

```python
def handler(request: Request, exc: MyException):
    # request: the incoming Request object
    # exc: the raised exception instance
    ...
```

> **One-liner:** *"Handler takes `request` and `exc`."*

### Q5: How do you handle `ValueError` globally?

**Answer:** Register a handler for it:

```python
@app.exception_handler(ValueError)
def value_error_handler(request, exc):
    return JSONResponse(400, {"error": "invalid_value", "detail": str(exc)})
```

Now any `raise ValueError(...)` inside any route returns a 400 with your shape.

> **One-liner:** *"Register a handler for any built-in exception type."*

### Q6: What's the difference between a custom exception and `HTTPException`?

**Answer:**

| `HTTPException` | Custom exception |
|:----------------|:-----------------|
| Built into FastAPI | You define it |
| Carries `status_code` + `detail` | Carries whatever you put on it |
| One shape (`{detail}`) | Any shape you design |
| Inline definition | Centralized handler |
| Use for one-offs | Use for repeated patterns |

> **One-liner:** *"HTTPException for one-offs. Custom for patterns."*

### Q7: How do you override FastAPI's built-in 422 handler?

**Answer:** Use `RequestValidationError`:

```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def custom_422(request, exc):
    return JSONResponse(
        status_code=422,
        content={"error": "validation", "fields": exc.errors()}
    )
```

> **One-liner:** *"Override 422 with `RequestValidationError`."*

### Q8: Is catching `Exception` (catch-all) a good idea?

**Answer:** **Use with care.** Catching `Exception` swallows programmer bugs (KeyError, AttributeError) and masks problems. Use it as a **last-resort safety net** that logs the error and returns a generic 500.

```python
@app.exception_handler(Exception)
def last_resort(request, exc):
    logger.error(f"Unhandled: {exc}", exc_info=True)
    return JSONResponse(500, {"error": "internal"})
```

> **One-liner:** *"Catch-all = last resort, with logging."*

</div>