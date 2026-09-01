<div align="center">

# 👋 A002 — FastAPI Tutorial (Hello World)

### *The smallest possible app that teaches the biggest lesson.*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Difficulty](https://img.shields.io/badge/Level-Beginner-brightgreen?style=for-the-badge)
![Reading Time](https://img.shields.io/badge/Read_Time-15_min-blueviolet?style=for-the-badge)
![Lines of Code](https://img.shields.io/badge/Lines_of_Code-7-informational?style=for-the-badge)

</div>

---

## 🧠 The One-Sentence Summary

> **Three lines of code (`from fastapi import FastAPI`, `app = FastAPI()`, `@app.get("/")`) turn Python into a web server.**

That's the entire lesson. The rest of this README just unpacks it.

---

## 📑 Table of Contents

- [🧠 The One-Sentence Summary](#-the-one-sentence-summary)
- [📖 The 30-Second Story](#-the-30-second-story)
- [🎯 What You Will Learn (6 Skills)](#-what-you-will-learn-6-skills)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup (Mnemonic: VAPI)](#-installation--setup-mnemonic-vapi)
- [🧠 Anatomy of `main.py` — Line by Line](#-anatomy-of-mainpy--line-by-line)
- [🧠 The Three Layers (Mnemonic: VPC)](#-the-three-layers-mnemonic-vpc)
- [🛣️ API Endpoints](#-api-endpoints)
- [🧪 Try It (4 Different Ways)](#-try-it-4-different-ways)
- [🧠 Why Returning a Dict "Just Works"](#-why-returning-a-dict-just-works)
- [⚠️ Common Pitfalls & Fixes](#-common-pitfalls--fixes)
- [🧠 Mnemonic Cheat Sheet](#-mnemonic-cheat-sheet)
- [🧪 Recall Test](#-recall-test)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 📖 The 30-Second Story

You want Python to talk to the internet. Old way: write 200 lines of `socket` code. New way: import FastAPI, write 7 lines, run one command, visit `/docs` in your browser. That's the revolution FastAPI represents.

This module is the **shortest possible app** — but it teaches the **biggest lesson**: *type hints are enough.*

---

## 🎯 What You Will Learn (6 Skills)

| # | 🎯 Skill | 🧠 Why it sticks |
|:-:|:---------|:----------------|
| 1 | 📥 Install FastAPI + Uvicorn | "VAPI" mnemonic |
| 2 | 🏗️ Create the `app` instance | "The skeleton" metaphor |
| 3 | 🛣️ Decorate a function with `@app.get("/")` | "Registering a phone number" |
| 4 | 📤 Return a dict, get JSON back | "The chef never plates the food" |
| 5 | 🚀 Run Uvicorn with `--reload` | "Hot-reload = save & forget" |
| 6 | 🎨 Visit `/docs` for Swagger UI | "Your API is also a website" |

---

## 📂 Project Structure

```
📁 A002_FastAPI_Tutorial/
├── 🐍 main.py     ← the whole app (7 lines!)
└── 📖 README.md   ← you are here
```

> 💡 Notice there's **no** `requirements.txt`. That forces you to learn the install command by heart. (It's `pip install "fastapi[standard]"` — see below.)

---

## ⚙️ Installation & Setup (Mnemonic: **VAPI**)

> 🧠 **VAPI = Venv, Activate, Pip-install, Import.** Say it out loud. Repeat 3 times. Never forget.

### 1️⃣ V — Virtual environment
```powershell
python -m venv .venv
```

This creates an isolated Python "bubble" so packages don't fight each other.

### 2️⃣ A — Activate it
```powershell
.\.venv\Scripts\Activate.ps1
```

Your prompt now starts with `(.venv)`. That means "I'm in my bubble."

### 3️⃣ P — Pip-install FastAPI with extras
```powershell
pip install "fastapi[standard]"
```

The `[standard]` adds: `uvicorn` (server), `httpx` (test client), `jinja2` (templates), `python-multipart` (forms), `email-validator` (EmailStr).

### 4️⃣ I — Import FastAPI in code (already in main.py)
```python
from fastapi import FastAPI
```

### ▶️ Launch the dev server
```powershell
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

> 🧠 The three arguments: **`uvicorn main:app`** means *file `main.py`, object `app`*. **`--reload`** means *watch for file changes and restart automatically*.

---

## 🧠 Anatomy of `main.py` — Line by Line

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World from FastAPI venv"}
```

### Line 1 — Import
```python
from fastapi import FastAPI
```
Think of `FastAPI` as a **class** that knows how to:
- Register routes
- Validate input
- Serialize output
- Document itself

### Line 3 — App instance
```python
app = FastAPI()
```
`app` is the **single object** Uvicorn will serve. It holds your routes, exception handlers, middleware — everything.

> 🧠 **Metaphor:** Think of `app` as a *phone number*. Uvicorn dials it; FastAPI answers.

### Line 5 — Decorator
```python
@app.get("/")
```
This says: *"Whenever a `GET /` request arrives, call the function directly below."* Variants: `@app.post`, `@app.put`, `@app.delete`.

### Lines 6–7 — Handler
```python
def home():
    return {"message": "Hello World from FastAPI venv"}
```
- `def home()` — a regular Python function. FastAPI supports both `def` and `async def`.
- `return {...}` — return *any* Python object; FastAPI serializes it to JSON.

### 🎯 If you remember ONE thing
> **Three things are mandatory: `app = FastAPI()`, a decorator, a function.** Skip any one and nothing works.

---

## 🧠 The Three Layers (Mnemonic: **VPC**)

Every FastAPI request flows through three layers:

```
┌───────────────────────────────────────────────┐
│  V — Validate: type hints check the input     │
│  P — Plate:   FastAPI wraps your return in JSON│
│  C — Cook:    Your function does the real work│
└───────────────────────────────────────────────┘
```

In A002 the **V** layer is trivial (no inputs), but it's the same code path.

> 🧠 **VPC = "Very Particular Chef"** — the chef only ever gets pre-validated, pre-plated orders.

---

## 🛣️ API Endpoints

| Method | Endpoint | Description | Response |
|:------:|:---------|:------------|:---------|
| 🟢 GET | `/` | Welcome message | `{ "message": "Hello World from FastAPI venv" }` |

That's it. One endpoint. But **one is enough to learn the framework.**

---

## 🧪 Try It (4 Different Ways)

### 1️⃣ Browser
Open <http://127.0.0.1:8000/>. You'll see the JSON directly.

### 2️⃣ curl
```bash
curl http://127.0.0.1:8000/
```

### 3️⃣ Swagger UI
Open <http://127.0.0.1:8000/docs>. Click the endpoint, then **"Try it out" → Execute**. You don't even need curl.

### 4️⃣ ReDoc
Open <http://127.0.0.1:8000/redoc> for a clean, reference-style view.

---

## 🧠 Why Returning a Dict "Just Works"

You might wonder: *"How does Python know to set the `Content-Type: application/json` header?"* The answer is **duck typing + Starlette**.

```python
return {"message": "Hello"}
    │
    ▼  FastAPI sees a dict
    │
    ▼  Calls json.dumps() on it
    │
    ▼  Wraps in a JSONResponse
    │
    ▼  Adds Content-Type: application/json
    │
    ▼  Sends 200 OK
```

You didn't ask for any of that. FastAPI did it because **the framework's job is to handle HTTP so you don't have to.**

> 🧠 **Mental model:** You're a chef 🍳. You put food on a plate. The waiter (FastAPI) brings forks, napkins, and a bill. You never touch those.

---

## ⚠️ Common Pitfalls & Fixes

| 😖 Symptom | 🔍 Cause | ✅ Fix |
|:-----------|:---------|:------|
| `ModuleNotFoundError: No module named 'fastapi'` | Forgot to activate venv | `.\.venv\Scripts\Activate.ps1` |
| `Address already in use` | Another process on port 8000 | `uvicorn main:app --port 8001` |
| Browser shows blank | You hit `/docs` accidentally | Hit `/` instead |
| Code change doesn't appear | Forgot `--reload` | Add `--reload` flag |
| `python` not recognized | Python not in PATH | Reinstall Python and check "Add to PATH" |

### 🎯 If you remember ONE thing
> **Most beginner errors are environment errors, not code errors.** Activate the venv first, debug the code second.

---

## 🧠 Mnemonic Cheat Sheet

| Concept | Mnemonic | Story |
|:--------|:---------|:------|
| Install flow | **VAPI** | Venv, Activate, Pip, Import |
| Request flow | **VPC** | Validate, Plate, Cook |
| The 3 mandatory pieces | **ADF** | App, Decorator, Function |
| URL structure | **3 magic URLs** | `/`, `/docs`, `/redoc` |
| Why JSON just works | **"The waiter brings forks"** | Chef never touches them |

---

## 🧪 Recall Test

Close the README. On a blank page:

1. What does `app = FastAPI()` do?
2. What's the difference between `def` and `async def`?
3. What's the URL for Swagger UI?
4. What flag enables hot-reload?
5. Why does returning a dict return JSON?

> 5/5 → you've mastered the basics. 3/5 → re-read "Anatomy of main.py".

---

## 🚀 Where to Go Next

| Direction | Module |
|:----------|:-------|
| ⬅️ Back | [Root README](../README.md) |
| ⬅️ Previous | [A001](../A001_CrashCourse/) — CRUD |
| ➡️ Next | [A003](../A003_Built_First_FastAPI/) — Multi-route |
| ➡️ Future | [A004](../A004_Path_Parameter_Dynamic_Route_Validation/) — Path params |

---

<div align="center">

### 🚀 *"Hello, World." — Python, now speaking HTTP.* 🚀

Made with ❤️ and only 7 lines of code.

</div>