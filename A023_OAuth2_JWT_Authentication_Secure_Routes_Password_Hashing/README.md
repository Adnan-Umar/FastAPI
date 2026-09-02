<div align="center">

# 🔐 A023 — OAuth2 + JWT + Password Hashing

### *Form-encoded login. Hashed passwords. Bearer-token-protected routes.*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OAuth2](https://img.shields.io/badge/OAuth2-Password_Flow-orange?style=for-the-badge)
![JWT](https://img.shields.io/badge/JWT-HS256-000000?style=for-the-badge)
![passlib](https://img.shields.io/badge/passlib-sha256__crypt-blue?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Level-Intermediate-orange?style=for-the-badge)
![Reading Time](https://img.shields.io/badge/Read_Time-55_min-blueviolet?style=for-the-badge)

</div>

---

## 🧠 The One-Sentence Summary

> **Login uses an OAuth2 form (not JSON) to exchange username + password for a JWT; passwords are never stored in plain text — they're hashed with `passlib`; protected routes require `Authorization: Bearer <token>` and a valid, unexpired signature.**

If you remember *"**F-H-B-V** — **F**orm login, **H**ash, **B**earer, **V**erify"*, the rest of this README is decoration.

---

## 📑 Table of Contents

- [🧠 The One-Sentence Summary](#-the-one-sentence-summary)
- [📖 The Story: The Club with a Members List](#-the-story-the-club-with-a-members-list)
- [🎯 What You Will Learn (10 Skills)](#-what-you-will-learn-10-skills)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧬 Anatomy of `main.py` — Line by Line (Heavily Commented)](#-anatomy-of-mainpy--line-by-line-heavily-commented)
- [🛣️ API Endpoints](#-api-endpoints)
- [🧠 The Mental Model: How OAuth2 + JWT Works](#-the-mental-model-how-oauth2--jwt-works)
- [🆕 Every New Keyword Explained](#-every-new-keyword-explained)
- [🆚 A022 vs A023](#-a022-vs-a023)
- [🆚 Plain Password vs Hashed Password](#-plain-password-vs-hashed-password)
- [🧪 Try It With curl](#-try-it-with-curl)
- [🔧 Variations](#-variations)
- [⚠️ Common Pitfalls & Fixes](#-common-pitfalls--fixes)
- [🧠 Mnemonic Cheat Sheet](#-mnemonic-cheat-sheet)
- [🧪 Recall Test](#-recall-test)
- [🎯 Interview Q&A](#-interview-qa)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 📖 The Story: The Club with a Members List 🏛️

A022's concert was loose — anyone with a username/password could walk in, and the password was sent in cleartext. A023's club is stricter:

| A022 (loose) | A023 (strict) |
|:-------------|:--------------|
| 📨 Login = `?username=...&password=...` query string | 📨 Login = `application/x-www-form-urlencoded` body |
| 📒 Passwords stored as `"1234"` | 📒 Passwords stored as `"$sha256$5000$...$..."` (hashed) |
| 🎫 Token in custom `token: ...` header | 🎫 Token in standard `Authorization: Bearer ...` header |
| 🪪 No Swagger "Authorize" button | 🪪 Swagger "Authorize" button works out of the box |
| ⏱️ 30 min, hardcoded | ⏱️ 30 min, configurable via `ACCESS_TOKEN_EXPIRE_MINUTES` |
| 🪤 Catches **everything** (bare `except`) | 🪤 Catches **`JWTError`** only |

> 🧠 **Mnemonic:** "**F-H-B-V** — **F**orm login, **H**ash, **B**earer, **V**erify."

---

## 🎯 What You Will Learn (10 Skills)

| # | 🎯 Skill | 🧠 You'll remember it because... |
|:-:|:---------|:--------------------------------|
| 1 | 📨 **`OAuth2PasswordRequestForm`** | "Form-encoded body, not JSON" |
| 2 | 🪪 **`OAuth2PasswordBearer`** | "Adds Swagger Authorize + Bearer scheme" |
| 3 | 🔒 **`passlib.CryptContext`** | "The password hasher factory" |
| 4 | 🧂 **`hash_password()`** | "One-way transform" |
| 5 | 🧐 **`verify_password()`** | "Constant-time compare" |
| 6 | 🎫 **`Authorization: Bearer …`** | "The standard header" |
| 7 | ⏱️ **`ACCESS_TOKEN_EXPIRE_MINUTES`** | "Don't hardcode 30" |
| 8 | 🚨 **`JWTError` (specific)** | "Not bare `except`" |
| 9 | 🪤 **Lazy init for hashes** | "Compute on first use, not at import" |
| 10 | 🧪 **Form vs JSON vs query** | "OAuth2 = form" |

---

## 📂 Project Structure

```
📁 A023_OAuth2_JWT_Authentication_Secure_Routes_Password_Hashing/
├── 🐍 main.py             ← 130 lines: config + hashing + login + verify + /secure
├── 📦 requirements.txt    ← fastapi[standard] + python-jose + passlib
└── 📖 README.md           ← you are here
```

---

## ⚙️ Installation & Setup

```powershell
cd D:\AllProgram\LEARN\Python\FastAPI\A023_OAuth2_JWT_Authentication_Secure_Routes_Password_Hashing
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open <http://127.0.0.1:8000/docs> and try the **🔓 Authorize** button (top right).

---

## 🧬 Anatomy of `main.py` — Line by Line (Heavily Commented)

The full file is now annotated. Here's the **new / changed** portion (vs A022):

```python
# =========================================================
# A023 — OAuth2 + JWT + Password Hashing
# =========================================================
# Production-shaped auth flow:
#   - POST /login              → OAuth2PasswordRequestForm (form-encoded),
#                                verifies the password against a hashed one,
#                                returns a signed JWT (HS256, exp claim)
#   - GET  /secure             → requires a valid JWT in the Authorization
#                                header (Authorization: Bearer <token>)
#   - Passwords are NEVER stored in plain text — passlib hashes them
# =========================================================

# --- FastAPI: framework + HTTP errors + DI ---
from fastapi import FastAPI, HTTPException, Depends

# --- FastAPI security: OAuth2 form helper + Bearer token scheme ---
# OAuth2PasswordRequestForm reads `username` & `password` from an
#   application/x-www-form-urlencoded body (NOT a JSON body).
# OAuth2PasswordBearer tells Swagger UI to add the "Authorize" button
#   and tells clients to send `Authorization: Bearer <token>`.
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# --- python-jose: encode and decode JWTs ---
# "jose" = Javascript Object Signing and Encryption
from jose import jwt, JWTError
```

| Section | Code | 🧠 Why it's there |
|:--------|:-----|:------------------|
| Imports | `OAuth2PasswordRequestForm` | Read form-encoded body |
| Imports | `OAuth2PasswordBearer` | Bearer header + Swagger Authorize |
| Imports | `JWTError` | Specific exception to catch |
| Config | `ACCESS_TOKEN_EXPIRE_MINUTES = 30` | One source of truth |
| Hashing | `pwd_context = CryptContext(schemes=["sha256_crypt"])` | The hasher |
| Lazy init | `_initialize_user_db()` | Hash the seed password on first login |
| Helpers | `hash_password()` / `verify_password()` | Pure functions |
| Create token | `create_token(data, expires_minutes=...)` | No more hardcoded 30 |
| Login | `@app.post("/login")` with `OAuth2PasswordRequestForm` | Form body, not query |
| Verify | `Depends(oauth2_scheme)` | Reads `Authorization: Bearer …` |
| Verify | `except JWTError:` | Catches only JWT issues |

### The Five Magic Pieces

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")                  # Bearer scheme
pwd_context = CryptContext(schemes=["sha256_crypt"])                     # Hasher
pwd_context.hash("1234")                                                # Hash
pwd_context.verify(plain, hashed)                                       # Verify
form_data: OAuth2PasswordRequestForm = Depends()                        # Form body
```

> 🧠 **Mnemonic:** "**Scheme → Hash → Verify → Form.**"

### 🎯 If you remember ONE thing
> **OAuth2 = form body + Bearer header. Hash passwords with passlib. Catch `JWTError`, not bare `except`.**

---

## 🛣️ API Endpoints

| Method | Endpoint | Auth | Body | Returns |
|:------:|:---------|:----:|:-----|:--------|
| 🟡 POST | `/login` | none | `application/x-www-form-urlencoded` (`username=...&password=...`) | `{access_token, token_type: "bearer"}` or 400 |
| 🟢 GET | `/secure` | `Authorization: Bearer <token>` | — | `{message, data: {username}}` or 401 |

---

## 🧠 The Mental Model: How OAuth2 + JWT Works

```mermaid
sequenceDiagram
    participant C as Client
    participant F as FastAPI
    participant P as passlib
    participant J as jose.jwt

    Note over C,F: 1. LOGIN (form-encoded body)
    C->>F: POST /login  body: username=admin&password=1234
    F->>F: OAuth2PasswordRequestForm binds form_data
    F->>P: pwd_context.verify("1234", fake_user_db["admin"]["hashed_password"])
    P-->>F: True
    F->>J: jwt.encode({sub: "admin", exp: now+30m}, SECRET, "HS256")
    J-->>F: "eyJ..."
    F-->>C: {access_token: "eyJ...", token_type: "bearer"}

    Note over C,F: 2. PROTECTED REQUEST (Bearer header)
    C->>F: GET /secure   Authorization: Bearer eyJ...
    F->>F: Depends(oauth2_scheme) extracts the token
    F->>J: jwt.decode(eyJ..., SECRET, ["HS256"])
    J->>J: verify signature + check exp
    J-->>F: {sub: "admin", exp: ...}
    F-->>C: {message: "Hello you have access to secure data!", data: {username: "admin"}}
```

> 🧠 **The form is parsed by FastAPI's `OAuth2PasswordRequestForm` — the client sends `application/x-www-form-urlencoded`, NOT JSON.**

---

## 🆕 Every New Keyword Explained

### 1. `OAuth2PasswordRequestForm` — form body helper

**What:** A FastAPI dependency that parses `username` and `password` from a `application/x-www-form-urlencoded` body. This is the **OAuth2 password flow** body type.

```python
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
```

Client:

```bash
curl -X POST http://127.0.0.1:8000/login \
  -d "username=admin&password=1234"
#   ↑ note: no Content-Type: application/json; the default IS form-encoded
```

> 🧠 **Mnemonic:** "**OAuth2 = form. JSON = custom login.**"

### 2. `OAuth2PasswordBearer` — Bearer scheme

**What:** A FastAPI class that:

1. Tells Swagger UI to add the **🔓 Authorize** button
2. Declares the OpenAPI scheme as `bearerAuth`
3. When used as a dependency, extracts the token from `Authorization: Bearer <token>`

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_token(token: str = Depends(oauth2_scheme)):
    ...
```

> 🧠 **Mnemonic:** "**`OAuth2PasswordBearer` = 'Bearer header + Swagger Authorize'.**"

### 3. `passlib.CryptContext` — the hasher factory

**What:** A passlib object that wraps one or more hashing algorithms and handles the verification automatically.

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["sha256_crypt"])
```

> 🧠 **Mnemonic:** "**`CryptContext` = a box of hashers.**"

### 4. `pwd_context.hash(plain)` — hash a password

**What:** Returns a self-describing hash string (algorithm + salt + digest). The salt is **random** — same input gives a different hash each time.

```python
h = pwd_context.hash("1234")
# "$5$rounds=5000$3J4kL...long...$abc..."
```

> 🧠 **Mnemonic:** "**`hash` = one-way, salted, slow.**"

### 5. `pwd_context.verify(plain, hashed)` — verify a password

**What:** Re-hashes `plain` with the salt + algorithm embedded in `hashed`, then compares in **constant time** (to avoid timing attacks).

```python
pwd_context.verify("1234", "$5$rounds=5000$...$...")    # True
pwd_context.verify("5678", "$5$rounds=5000$...$...")    # False
```

> 🧠 **Mnemonic:** "**`verify` = constant-time compare.**"

### 6. `sha256_crypt` — passlib's pure-Python scheme

**What:** A SHA-256-based password hashing scheme. Pure-Python, no native deps, works on all modern Python versions (including 3.13/3.14 where `bcrypt` has compatibility issues).

| Scheme | Pros | Cons |
|:-------|:-----|:-----|
| `bcrypt` | Industry standard | Native dep; has issues on Python 3.14+ |
| `sha256_crypt` | Pure Python, portable | Slightly faster (slightly weaker) |
| `argon2` | State of the art | Extra dep: `argon2-cffi` |

> 🧠 **Mnemonic:** "**`sha256_crypt` = 'works everywhere'.**"

### 7. `Authorization: Bearer <token>` — standard header

**What:** The HTTP-standard way to send an access token. `<token>` is the JWT (or any opaque token).

```bash
curl -H "Authorization: Bearer eyJ..." http://127.0.0.1:8000/secure
```

> 🧠 **Mnemonic:** "**Bearer = 'whoever holds this is allowed'.**"

### 8. `ACCESS_TOKEN_EXPIRE_MINUTES` — expiry constant

**What:** A module-level constant controlling token lifetime. Used by `create_token` and visible to anyone reading the code.

```python
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(data, expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES):
    ...
```

> 🧠 **Mnemonic:** "**Constants at the top, not buried in functions.**"

### 9. `JWTError` — specific exception

**What:** The base class for all `python-jose` JWT errors. Catch **this** instead of bare `except`.

```python
from jose import JWTError

try:
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
except JWTError:    # ← specific
    raise HTTPException(401, "Invalid or expired token")
```

Subclasses you might also see: `ExpiredSignatureError`, `JWTClaimsError`.

> 🧠 **Mnemonic:** "**Catch `JWTError`, not `Exception`.**"

### 10. Lazy initialization

**What:** Compute the password hash on the **first login attempt**, not at import time. This sidesteps issues with passlib taking a long time at import, or import-time side effects.

```python
def _initialize_user_db():
    if fake_user_db["admin"]["hashed_password"] is None:
        fake_user_db["admin"]["hashed_password"] = pwd_context.hash("1234")
```

> 🧠 **Mnemonic:** "**Hash on first use, not at import.**"

---

## 🆚 A022 vs A023

| Aspect | A022 | A023 |
|:-------|:-----|:-----|
| Login body | Query string `?username=...&password=...` | Form `application/x-www-form-urlencoded` |
| `Depends` for login | None (just query params) | `OAuth2PasswordRequestForm` |
| Token transport | Custom `token: …` header | Standard `Authorization: Bearer …` |
| Swagger Authorize button | ❌ | ✅ |
| Password storage | Plain text comparison | Hashed (passlib) |
| `except` | Bare `except` | Specific `JWTError` |
| Expiry config | Hardcoded 30 | `ACCESS_TOKEN_EXPIRE_MINUTES` constant |
| Required deps | `fastapi[standard]`, `python-jose` | + `passlib` |

> 🧠 **Mnemonic:** "**A023 = A022 + form + hash + Bearer + Authorize button.**"

---

## 🆚 Plain Password vs Hashed Password

| Aspect | Plain `"1234"` | Hashed `"$5$...$...$..."` |
|:-------|:----------------|:--------------------------|
| Reversible? | ✅ trivial (it's the password) | ❌ practically impossible |
| Two users with the same password look the same in DB? | ✅ (info leak) | ❌ different salts |
| DB leak impact? | Total compromise | Attackers must brute-force each hash individually |
| Speed of compare? | `==` | `pwd_context.verify()` (slow on purpose) |
| Constant-time compare? | ❌ `==` is not constant-time | ✅ `verify` is |

> 🧠 **Mnemonic:** "**Hash = one-way, salted, slow on purpose.**"

---

## 🧪 Try It With curl

### 1. Try to access `/secure` without a token (401)

```bash
curl -i http://127.0.0.1:8000/secure
```

```http
HTTP/1.1 401 Not Found   (or 401, depending on the framework's default)
{"detail": "Not authenticated"}
```

> ℹ️ FastAPI returns 401 here because `OAuth2PasswordBearer` raises when the header is missing.

### 2. Log in with wrong creds (400)

```bash
curl -i -X POST http://127.0.0.1:8000/login \
  -d "username=admin&password=wrong"
```

```http
HTTP/1.1 400 Bad Request
{"detail":"Invalid username or password"}
```

### 3. Log in with good creds (200)

```bash
curl -X POST http://127.0.0.1:8000/login \
  -d "username=admin&password=1234"
```

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcyNTI0OTI4MH0.xxx",
  "token_type": "bearer"
}
```

### 4. Save the token and hit `/secure` (200)

```bash
# PowerShell
$TOKEN = (curl -X POST http://127.0.0.1:8000/login -d "username=admin&password=1234" | ConvertFrom-Json).access_token
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/secure
```

```json
{
  "message": "Hello you have access to secure data!",
  "data": {"username": "admin"}
}
```

### 5. Hit `/secure` with a tampered token (401)

```bash
curl -H "Authorization: Bearer eyJxxx.tampered.signature" http://127.0.0.1:8000/secure
```

```http
HTTP/1.1 401 Unauthorized
{"detail":"Invalid or expired token"}
```

---

## 🔧 Variations

### Variation 1: Add a `/register` endpoint that hashes the password

```python
from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    password: str

@app.post("/register", status_code=201)
def register(body: RegisterRequest):
    if body.username in fake_user_db:
        raise HTTPException(400, "User already exists")
    fake_user_db[body.username] = {
        "username": body.username,
        "hashed_password": hash_password(body.password),
    }
    return {"message": "User registered"}
```

### Variation 2: Refresh token (long-lived)

```python
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_refresh_token(sub: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return jwt.encode({"sub": sub, "type": "refresh", "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_user_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(400, "Invalid credentials")
    return {
        "access_token": create_token({"sub": user["username"], "type": "access"}),
        "refresh_token": create_refresh_token(user["username"]),
        "token_type": "bearer",
    }
```

### Variation 3: Add scopes / roles

```python
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scopes={"read": "Read access", "write": "Write access", "admin": "Admin access"},
)

def require_scopes(*required: str):
    def dep(user: dict = Depends(verify_token)):
        token_scopes = user.get("scopes", [])
        if not all(s in token_scopes for s in required):
            raise HTTPException(403, "Missing scope")
        return user
    return dep

@app.get("/admin")
def admin_route(user: dict = Depends(require_scopes("admin"))):
    return {"message": "admin only", "user": user}
```

### Variation 4: Multiple users

```python
fake_user_db: dict[str, dict] = {}

@app.post("/register", status_code=201)
def register(body: RegisterRequest):
    if body.username in fake_user_db:
        raise HTTPException(400, "User exists")
    fake_user_db[body.username] = {
        "username": body.username,
        "hashed_password": hash_password(body.password),
    }
    return {"message": "registered"}

# In login(), remove the _initialize_user_db() call
```

### Variation 5: Switch to `bcrypt` if you have it installed

```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

If you hit the `bcrypt` 5.x + Python 3.14 issue, pin `bcrypt<4` or use `sha256_crypt` (this module's default).

---

## ⚠️ Common Pitfalls & Fixes

| 😖 Pitfall | 🔍 Cause | ✅ Fix |
|:-----------|:---------|:------|
| 422 "field required" on login | Sent JSON body instead of form | Send `application/x-www-form-urlencoded` with `-d "username=...&password=..."` |
| 401 on `/secure` even with valid token | Custom header used; oauth2_scheme expects `Authorization: Bearer …` | Send `Authorization: Bearer <token>` |
| Hash takes forever at import time | Initializing hash at module level | Use lazy init (this module's pattern) |
| `bcrypt` warnings on Python 3.14 | `bcrypt` 5.x incompatibility | Use `sha256_crypt` (default) or `argon2` |
| `except` catches everything | Bare `except:` | `except JWTError:` specifically |
| Login returns 200 with wrong creds | Forgot to call `verify_password` | Always go through `pwd_context.verify(plain, hashed)` |
| `pwd_context.hash` returns the same value twice | Old passlib + bcrypt bug | Update passlib, or use `sha256_crypt` |
| Leaking which field is wrong | "Invalid username" vs "Invalid password" | Use the same message for both |
| Token never expires | `exp` claim missing or in the past | `datetime.now(timezone.utc) + timedelta(...)` |

### The "JSON vs Form" Trap

```python
# ❌ This won't work — login expects form-encoded, not JSON
@app.post("/login")
def login(body: LoginRequest):  # LoginRequest is a Pydantic JSON model
    ...

# ✅ Use the OAuth2 form dependency
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    ...
```

Client:

```bash
# ❌ Wrong
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"1234"}'

# ✅ Right
curl -X POST http://127.0.0.1:8000/login \
  -d "username=admin&password=1234"
```

### The "Bearer vs Custom Header" Trap

```bash
# ❌ Wrong — A022 used a custom header; A023 uses Bearer
curl -H "token: eyJ..." http://127.0.0.1:8000/secure

# ✅ Right
curl -H "Authorization: Bearer eyJ..." http://127.0.0.1:8000/secure
```

### The "Bare `except`" Trap

```python
# ❌ Catches KeyboardInterrupt, SystemExit, etc.
try:
    payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
except:
    raise HTTPException(401, "Invalid")

# ✅ Catches only JWT issues
from jose import JWTError
try:
    payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
except JWTError:
    raise HTTPException(401, "Invalid or expired token")
```

> 🧠 **Mnemonic:** "**Form body, Bearer header, `JWTError` only.**"

---

## 🧠 Mnemonic Cheat Sheet

| Concept | Mnemonic | Story |
|:--------|:---------|:------|
| 4-step flow | **F-H-B-V** | Form, Hash, Bearer, Verify |
| OAuth2 form | **Form body, not JSON** | `application/x-www-form-urlencoded` |
| `OAuth2PasswordBearer` | **Bearer + Authorize button** | Adds Swagger UI |
| `CryptContext` | **Box of hashers** | One object, many schemes |
| `hash` | **One-way, salted, slow** | Same input → different output |
| `verify` | **Constant-time compare** | Avoids timing attacks |
| `sha256_crypt` | **Works everywhere** | Pure Python, no native deps |
| `Authorization: Bearer` | **Standard header** | Not `token: ...` |
| `JWTError` | **Catch this, not `except`** | Specific exception |
| Lazy init | **Hash on first use** | Not at import |
| Form vs JSON | **OAuth2 = form** | `application/x-www-form-urlencoded` |

---

## 🧪 Recall Test

1. What body type does `OAuth2PasswordRequestForm` expect?
2. What header carries the JWT in A023?
3. What's the role of `OAuth2PasswordBearer`?
4. How do you hash a password with passlib?
5. How do you verify a password with passlib?
6. Why use `sha256_crypt` instead of `bcrypt` here?
7. Why catch `JWTError` instead of bare `except`?
8. What is the A023 "Author -> Bearer -> decode" flow?

> 8/8 → OAuth2 + JWT + hashing is yours.

---

## 🎯 Interview Q&A

### Q1: What's the difference between A022's login and A023's login?

**Answer:**

| A022 | A023 |
|:-----|:-----|
| Query string `?username=...&password=...` | Form body `application/x-www-form-urlencoded` |
| Plain-text password comparison | Hashed password comparison |
| Custom `token:` header | Standard `Authorization: Bearer …` header |
| No Swagger Authorize | Swagger Authorize works |

> **One-liner:** *"A023 = A022 + form body + hashed passwords + Bearer header."*

### Q2: What is `OAuth2PasswordRequestForm`?

**Answer:** A FastAPI dependency that parses `username` and `password` from a `application/x-www-form-urlencoded` body. It is the **OAuth2 password flow** body type, the one the spec defines.

> **One-liner:** *"Reads the OAuth2-spec form body."*

### Q3: What is `OAuth2PasswordBearer`?

**Answer:** A FastAPI class that:

1. Declares the OpenAPI `bearerAuth` security scheme
2. Adds Swagger UI's **🔓 Authorize** button
3. When used as a dependency, extracts the token from `Authorization: Bearer <token>`

> **One-liner:** *"Bearer scheme + Swagger Authorize button."*

### Q4: How do you hash and verify passwords with passlib?

**Answer:**

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["sha256_crypt"])

hashed = pwd_context.hash("1234")                  # one-way, salted
ok = pwd_context.verify("1234", hashed)            # True
ok = pwd_context.verify("5678", hashed)            # False
```

> **One-liner:** *"`hash` to create, `verify` to check, in constant time."*

### Q5: Why use `sha256_crypt` instead of `bcrypt`?

**Answer:** `bcrypt` 5.x has compatibility issues with Python 3.14+. `sha256_crypt` is pure-Python, has no native dependencies, and works on all modern Python versions.

| Scheme | Python 3.14? | Native dep? |
|:-------|:-------------|:------------|
| `bcrypt` 5.x | ⚠️ issues | Yes |
| `sha256_crypt` | ✅ | No |
| `argon2` | ✅ | Yes (`argon2-cffi`) |

> **One-liner:** *"`sha256_crypt` = works everywhere, no native deps."*

### Q6: Why catch `JWTError` instead of bare `except`?

**Answer:** Bare `except` catches **everything** — `KeyboardInterrupt`, `SystemExit`, `MemoryError`, etc. — which can hide bugs. `JWTError` is the specific base class for `python-jose` errors, so you only catch JWT problems.

```python
# ❌ too broad
try:
    payload = jwt.decode(...)
except:
    raise HTTPException(401, "Invalid")

# ✅ specific
from jose import JWTError
try:
    payload = jwt.decode(...)
except JWTError:
    raise HTTPException(401, "Invalid or expired token")
```

> **One-liner:** *"Catch `JWTError`, not everything."*

### Q7: What is the standard header for sending a JWT?

**Answer:** `Authorization: Bearer <token>`. This is the HTTP standard (RFC 6750). A022's custom `token: …` header is non-standard and won't work with most clients or proxies.

> **One-liner:** *"Bearer header, not custom."*

### Q8: How do you add scopes / roles to a JWT?

**Answer:** Put them in the payload at login, then check them in a `require_scopes` dependency:

```python
# Login: include scopes
return create_token({"sub": username, "scopes": ["read", "write"]})

# Verify: check scopes
def require_scopes(*required):
    def dep(user=Depends(verify_token)):
        if not all(s in user.get("scopes", []) for s in required):
            raise HTTPException(403, "Missing scope")
        return user
    return dep

@app.get("/admin")
def admin(user=Depends(require_scopes("admin"))):
    ...
```

> **One-liner:** *"Scopes go in the payload; check them in a dep."*

---

## 🚀 Where to Go Next

| Direction | Module |
|:----------|:-------|
| ⬅️ Previous | [A022](../A022_JWT_Authentication_Token_Based_Auth_Login_API/) |
| ⬅️ Back | [Root README](../README.md) |
| ➡️ Next | A024 (planned) — RBAC with role-based dependencies |
| ➡️ Future | A025 (planned) — Refresh tokens + blocklist |

---

<div align="center">

### 🔐 *Form login. Hash passwords. Bearer token. Verify.* 🔐

Made with ❤️, `OAuth2PasswordRequestForm`, `pwd_context.hash(...)`, and `Depends(oauth2_scheme)`.

</div>