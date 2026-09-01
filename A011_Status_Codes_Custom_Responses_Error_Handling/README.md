<div align="center">

# 🚦 A011 — Status Codes, Custom Responses & Error Handling

### *200 is just the beginning. Learn to speak fluent HTTP.*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/HTTP_Status_Codes-✅-success?style=for-the-badge)
![Errors](https://img.shields.io/badge/Error_Handling-🛡️-red?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Level-Intermediate-orange?style=for-the-badge)
![Reading Time](https://img.shields.io/badge/Read_Time-45_min-blueviolet?style=for-the-badge)

</div>

---

## 🧠 The One-Sentence Summary

> **HTTP status codes are the language servers use to say "yes", "no", "maybe", and "I broke"; FastAPI gives you `status_code=` for the first response and `HTTPException` for the second.**

If you remember *"status_code = happy path, HTTPException = error path"*, the rest of this README is decoration.

---

## 📑 Table of Contents

- [🧠 The One-Sentence Summary](#-the-one-sentence-summary)
- [📖 The Story: The Restaurant Order](#-the-story-the-restaurant-order)
- [🎯 What You Will Learn (12 Skills)](#-what-you-will-learn-12-skills)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧬 Anatomy of `main.py` — Line by Line](#-anatomy-of-mainpy--line-by-line)
- [🛣️ API Endpoints](#-api-endpoints)
- [🧠 The Mental Model: Every Response Is a Story](#-the-mental-model-every-response-is-a-story)
- [🔢 The HTTP Status Code Cheat Sheet](#-the-http-status-code-cheat-sheet)
- [🚨 Deep Dive: `HTTPException`](#-deep-dive-httpexception)
- [🎨 Deep Dive: Custom Response Shapes](#-deep-dive-custom-response-shapes)
- [🧪 Try It With curl](#-try-it-with-curl)
- [🔧 Variations You Should Know](#-variations-you-should-know)
- [⚠️ Common Pitfalls & Fixes](#-common-pitfalls--fixes)
- [🧠 Mnemonic Cheat Sheet](#-mnemonic-cheat-sheet)
- [🧪 Recall Test](#-recall-test)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 📖 The Story: The Restaurant Order

Imagine a waiter 🍽️ at a restaurant. When you order, the waiter says things like:

- ✅ *"Your food is coming!"* → **`200 OK`**
- 🆕 *"Order placed, kitchen got it!"* → **`201 Created`**
- 🔍 *"Sorry, that dish isn't on the menu."* → **`404 Not Found`**
- 💥 *"The kitchen is on fire."* → **`500 Internal Server Error`**

The waiter doesn't just bring food — they tell you **what happened** with the right words. HTTP status codes are those words. FastAPI gives you two tools:

| Tool | When to use | Story |
|:-----|:------------|:------|
| `status_code=...` | When things go **right** | The waiter's normal announcements |
| `raise HTTPException(...)` | When things go **wrong** | The waiter explaining a problem |

> 🧠 **Mnemonic:** "**200 = chef cooks, 500 = chef quits.**"

---

## 🎯 What You Will Learn (12 Skills)

| # | 🎯 Skill | 🧠 You'll remember it because... |
|:-:|:---------|:--------------------------------|
| 1 | 🔢 **Status code basics** | "5 categories: 1xx–5xx" |
| 2 | ✅ **200 OK default** | "Default success" |
| 3 | 🆕 **201 Created for POST** | "Convention: new resource" |
| 4 | 🚨 **HTTPException basics** | "Raise, don't return" |
| 5 | 🔍 **404 Not Found** | "The most common error" |
| 6 | 🛡️ **Custom `detail` field** | "Tell the client what went wrong" |
| 7 | 🎨 **Custom response shape** | "{status, message, data}" pattern |
| 8 | 🧰 **`from fastapi import status`** | "Magic numbers as readable constants" |
| 9 | 🪜 **Layered error handling** | "Validation → HTTPException → custom" |
| 10 | 📤 **Headers in responses** | "Set Location on 201" |
| 11 | 🛑 **Common status codes cheat sheet** | "200, 201, 204, 400, 401, 403, 404, 422, 500" |
| 12 | 🧠 **Idempotency of GET vs POST** | "GET = safe, POST = create" |

---

## 📂 Project Structure

```
📁 A011_Status_Codes_Custom_Responses_Error_Handling/
├── 🐍 main.py     ← 36 lines, 3 endpoints, 3 patterns
└── 📖 README.md   ← you are here
```

---

## ⚙️ Installation & Setup

```powershell
cd D:\AllProgram\LEARN\Python\FastAPI\A011_Status_Codes_Custom_Responses_Error_Handling
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "fastapi[standard]"
uvicorn main:app --reload
```

Visit <http://127.0.0.1:8000/docs> — note the response codes shown next to each endpoint.

---

## 🧬 Anatomy of `main.py` — Line by Line

```python
from fastapi import FastAPI, status, HTTPException

app = FastAPI()

# Pattern 1: Custom status code on success
@app.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user():
    return {
        "message": "user created"
    }

# Pattern 2: Custom response shape
@app.get("/user")
def get_users():
    return {
        "status": "Success",
        "message": "User Fetched",
        "data": {
            "name": "Adnan",
            "age": 21
        }
    }

# Pattern 3: HTTPException for errors
@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not found"
        )

    return {
        "id": 1,
        "name": "Adnan"
    }
```

| Lines | Code | 🧠 Why it's there |
|:-----:|:-----|:------------------|
| 1 | Imports | FastAPI + `status` + `HTTPException` |
| 3 | `app = FastAPI()` | App instance |
| 5–10 | `POST /create_user` with `status_code=201` | **Pattern 1** — success with custom code |
| 12–22 | `GET /user` with structured response | **Pattern 2** — custom response shape |
| 24–36 | `GET /users/{user_id}` with `HTTPException` | **Pattern 3** — error handling |

### The Three Patterns at a Glance

| Pattern | Tool | When |
|:--------|:-----|:----|
| 1️⃣ Custom success code | `status_code=status.HTTP_201_CREATED` | The happy path needs a non-default code |
| 2️⃣ Custom response shape | Return a `dict` with `status`, `message`, `data` | You want richer response structure |
| 3️⃣ Error handling | `raise HTTPException(...)` | Something went wrong |

> 🧠 **Mnemonic:** "**S-R-E**" — **S**uccess (status_code=), **R**ich response (dict), **E**rror (HTTPException).

### 🎯 If you remember ONE thing
> **`status_code=` is for the happy path. `HTTPException` is for the unhappy path. Pick the right tool.**

---

## 🛣️ API Endpoints

| # | Method | Endpoint | Pattern | Status Codes |
|:-:|:------:|:---------|:--------|:-------------|
| 1 | 🟡 POST | `/create_user` | 1 — Custom success code | `201` |
| 2 | 🟢 GET | `/user` | 2 — Custom response shape | `200` |
| 3 | 🟢 GET | `/users/{user_id}` | 3 — Error handling | `200` or `404` |

---

### 1️⃣ `POST /create_user` — Custom Success Code

```bash
curl -i -X POST http://127.0.0.1:8000/create_user
```

```http
HTTP/1.1 201 Created                  ← not 200!
content-type: application/json
{"message":"user created"}
```

> 🧠 **Why 201?** Because convention says: *POST that creates a resource returns `201 Created`*.

### 2️⃣ `GET /user` — Custom Response Shape

```bash
curl http://127.0.0.1:8000/user
```

```json
{
  "status": "Success",
  "message": "User Fetched",
  "data": {
    "name": "Adnan",
    "age": 21
  }
}
```

The body has a `status`, `message`, and `data` field — a common API convention.

### 3️⃣ `GET /users/{user_id}` — Error Handling

```bash
# Success
curl http://127.0.0.1:8000/users/1
# {"id":1,"name":"Adnan"}

# Error
curl -i http://127.0.0.1:8000/users/99
```

```http
HTTP/1.1 404 Not Found
content-type: application/json
{"detail":"User Not found"}
```

> 🧠 **Note:** FastAPI wraps the `detail` in `{"detail": ...}` automatically.

---

## 🧠 The Mental Model: Every Response Is a Story

```
┌─────────────────────────────────────────────────────┐
│  Client sends:  GET /users/1                        │
│                                                     │
│  Your function runs:                                │
│    ├── Path validated ✓                             │
│    ├── Function executes                            │
│    └── Returns: { "id": 1, "name": "Adnan" }       │
│                                                     │
│  FastAPI chooses a status code:                     │
│    ├── Returned normally → 200 OK                   │
│    ├── raise HTTPException(404, ...) → 404          │
│    ├── Pydantic validation failed → 422             │
│    └── Unhandled exception → 500                    │
│                                                     │
│  Response shipped to client with chosen code        │
└─────────────────────────────────────────────────────┘
```

---

## 🔢 The HTTP Status Code Cheat Sheet

| Code | Name | When to use | FastAPI constant |
|:----:|:-----|:------------|:-----------------|
| 🟢 **200** | OK | Default for success | `status.HTTP_200_OK` |
| 🆕 **201** | Created | POST that creates something | `status.HTTP_201_CREATED` |
| 🛌 **204** | No Content | Success but no body (e.g. DELETE) | `status.HTTP_204_NO_CONTENT` |
| 🔄 **301** | Moved Permanently | Resource moved forever | `status.HTTP_301_MOVED_PERMANENTLY` |
| 🟡 **400** | Bad Request | Generic client error | `status.HTTP_400_BAD_REQUEST` |
| 🔐 **401** | Unauthorized | Not authenticated | `status.HTTP_401_UNAUTHORIZED` |
| 🚫 **403** | Forbidden | Authenticated but not allowed | `status.HTTP_403_FORBIDDEN` |
| 🔍 **404** | Not Found | Resource doesn't exist | `status.HTTP_404_NOT_FOUND` |
| ⚔️ **409** | Conflict | Duplicate / state conflict | `status.HTTP_409_CONFLICT` |
| 🛡️ **422** | Unprocessable Entity | Pydantic validation failed | `status.HTTP_422_UNPROCESSABLE_ENTITY` |
| 💥 **500** | Internal Server Error | You wrote a bug | `status.HTTP_500_INTERNAL_SERVER_ERROR` |
| 🛠️ **503** | Service Unavailable | Down for maintenance | `status.HTTP_503_SERVICE_UNAVAILABLE` |

### The 5 Categories (Mnemonic: "**T-S-R-C-S**")

| Range | Category | Mnemonic | Meaning |
|:------|:---------|:---------|:--------|
| **1xx** | Informational | **T**ell me more | Server is mid-thought |
| **2xx** | Success | **S**uccess! | "It worked." |
| **3xx** | Redirection | **R**edirect | "Look over there." |
| **4xx** | Client Error | **C**lient's fault | "You messed up." |
| **5xx** | Server Error | **S**erver's fault | "I messed up." |

> 🧠 **"Tell me more, Success, Redirect, Client's fault, Server's fault"** — five categories, one line.

---

## 🚨 Deep Dive: `HTTPException`

### The Basic Form

```python
from fastapi import HTTPException, status

raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User Not found"
)
```

FastAPI's response:

```json
{ "detail": "User Not found" }
```

with status `404`.

### The Anatomy of `HTTPException`

| Argument | Type | Required | Purpose |
|:---------|:-----|:---------|:--------|
| `status_code` | `int` | ✅ Yes | The HTTP code to return |
| `detail` | `Any` | ❌ No | What to put in the body (default: `"Internal Server Error"`) |
| `headers` | `dict` | ❌ No | Extra HTTP headers |

### Detail Can Be Anything JSON-Serializable

```python
# String
raise HTTPException(404, "User Not found")

# Dict (richer error info)
raise HTTPException(404, {"error": "user_not_found", "id": user_id})

# List
raise HTTPException(400, ["Invalid name", "Invalid age"])
```

### Adding Custom Headers

```python
raise HTTPException(
    status_code=401,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"}
)
```

### What `raise` Does

```python
if user_id != 1:
    raise HTTPException(...)   # ← execution STOPS here
                              # ← FastAPI catches the exception
                              # ← and returns the response

return {"id": 1, ...}         # ← never reached
```

> 🧠 **Mnemonic:** "**Raise = stop, return = go**" — `raise` kills the function; `return` ends it normally.

---

## 🎨 Deep Dive: Custom Response Shapes

### The `{status, message, data}` Pattern

```python
@app.get("/user")
def get_users():
    return {
        "status": "Success",
        "message": "User Fetched",
        "data": {"name": "Adnan", "age": 21}
    }
```

This is a common convention (especially in Indian API tutorials, which is where A011 originates). Real-world alternatives:

| Pattern | Used by |
|:--------|:--------|
| `{status, message, data}` | Many tutorials |
| `{data, meta: {total, page}}` | REST best practice |
| `{results: [...], count: N}` | Django REST framework |
| `{error: {code, message}}` | GitHub API |

### Combine with Pydantic for Type Safety

```python
from pydantic import BaseModel
from typing import Generic, TypeVar

class StandardResponse(BaseModel):
    status: str
    message: str
    data: dict

@app.get("/user", response_model=StandardResponse)
def get_users():
    return {
        "status": "Success",
        "message": "User Fetched",
        "data": {"name": "Adnan", "age": 21}
    }
```

Now FastAPI:
- ✅ Validates the response shape
- ✅ Documents it in `/docs`
- ✅ Filters extra fields

### 🎯 If you remember ONE thing
> **Custom shapes are just dicts. Pydantic + `response_model` makes them self-documenting.**

---

## 🧪 Try It With curl

```bash
# 1. POST that returns 201
curl -i -X POST http://127.0.0.1:8000/create_user

# 2. GET with custom response shape
curl http://127.0.0.1:8000/user

# 3. GET success
curl -i http://127.0.0.1:8000/users/1

# 4. GET 404 error
curl -i http://127.0.0.1:8000/users/99
```

### Use `-i` to see the status code

The `-i` flag includes response headers. Without it, you only see the body.

---

## 🔧 Variations You Should Know

### 1️⃣ Set `Location` header on 201

```python
from fastapi import Response

@app.post("/create_user", status_code=201)
def create_user(response: Response):
    response.headers["Location"] = "/users/1"
    return {"message": "user created", "id": 1}
```

### 2️⃣ Custom 422 handler

```python
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"error": "validation", "fields": exc.errors()}
    )
```

### 3️⃣ Global exception handler

```python
@app.exception_handler(Exception)
async def global_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "internal", "message": str(exc)}
    )
```

### 4️⃣ Use `JSONResponse` directly

```python
from fastapi.responses import JSONResponse

@app.get("/custom")
def custom():
    return JSONResponse(
        status_code=200,
        content={"custom": True},
        headers={"X-Custom": "value"}
    )
```

### 5️⃣ `HTTPException` with dict detail

```python
raise HTTPException(
    status_code=400,
    detail={
        "error": "invalid_input",
        "fields": ["name", "age"]
    }
)
```

Client sees:

```json
{"detail": {"error": "invalid_input", "fields": ["name", "age"]}}
```

### 6️⃣ Reuse error logic

```python
def not_found(what: str, id):
    return HTTPException(404, f"{what} with id={id} not found")

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id != 1:
        raise not_found("User", user_id)
    return {"id": 1, "name": "Adnan"}
```

---

## ⚠️ Common Pitfalls & Fixes

| 😖 Pitfall | 🔍 Cause | ✅ Fix |
|:-----------|:---------|:------|
| Always returns 200 even for errors | Returning a dict with `error` key | Use `raise HTTPException(...)` |
| `detail` shown as `[...]` list | You passed a list accidentally | Pass a string or dict |
| Custom handler not triggered | Wrong exception type | Use `RequestValidationError` for 422 |
| 500 errors leak stack trace | No global handler | Add `@app.exception_handler(Exception)` |
| `Response` parameter ignored | Forgot to import / wrong position | Must be a typed parameter |
| 201 response has no `Location` | Not setting header | Add `response.headers["Location"] = ...` |
| `raise` outside function | Used at module level | Always inside a function body |

---

## 🧠 Mnemonic Cheat Sheet

| Concept | Mnemonic | Story |
|:--------|:---------|:------|
| Three patterns | **S-R-E** | Success code, Rich response, Error |
| Categories | **T-S-R-C-S** | Tell me, Success, Redirect, Client, Server |
| `raise` vs `return` | **Raise = stop, return = go** | Two different paths |
| Detail wrapper | **"detail" is the magic key** | FastAPI wraps it for you |
| Convention | **POST → 201, GET → 200, DELETE → 204** | REST norms |
| Bouncer | **200 = chef cooks, 500 = chef quits** | Status codes are stories |

---

## 🧪 Recall Test

1. What's the default status code for a successful `GET`?
2. What status code should a successful `POST` return?
3. How do you return a `404` from inside a function?
4. What's the difference between `return` and `raise`?
5. What's the magic key in the 404 response body?
6. How do you import the `status` constants?
7. How do you add a custom header to a 201 response?

> 7/7 → you speak fluent HTTP.

---

## 🚀 Where to Go Next

| Direction | Module |
|:----------|:-------|
| ⬅️ Previous | [A010](../A010_Response_Models_Data_Validation_Hide_Sensitive_Data/) |
| ⬅️ Back | [Root README](../README.md) |
| ➡️ Next | A012 (planned) — Dependencies & Authentication |
| ➡️ Future | A013 (planned) — Database Integration with SQLAlchemy |

---

<div align="center">

### 🚦 *HTTP has a language. Now you speak it.* 🚦

Made with ❤️, 201s, and the occasional 404.

</div>