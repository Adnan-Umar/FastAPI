<div align="center">

# 🛣️ A003 — Building Your First FastAPI App

### *Three routes, one app, infinite possibilities.*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Difficulty](https://img.shields.io/badge/Level-Beginner-brightgreen?style=for-the-badge)
![Reading Time](https://img.shields.io/badge/Read_Time-20_min-blueviolet?style=for-the-badge)
![Endpoints](https://img.shields.io/badge/Endpoints-3-orange?style=for-the-badge)

</div>

---

## 🧠 The One-Sentence Summary

> **A route is a (URL path, HTTP method) pair bound to one Python function — and FastAPI lets you bind as many as you want on one `app`.**

If you remember just *"URL + method → function"*, this whole README is yours.

---

## 📑 Table of Contents

- [🧠 The One-Sentence Summary](#-the-one-sentence-summary)
- [📖 The 30-Second Story](#-the-30-second-story)
- [🎯 What You Will Learn (6 Skills)](#-what-you-will-learn-6-skills)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧠 Anatomy of `main.py` — Line by Line](#-anatomy-of-mainpy--line-by-line)
- [🛣️ API Endpoints](#-api-endpoints)
- [🧪 Try It](#-try-it)
- [📐 HTTP & Routing Concepts](#-http--routing-concepts)
- [⚠️ Common Pitfalls & Fixes](#-common-pitfalls--fixes)
- [🔧 Suggested Refactor](#-suggested-refactor)
- [🧠 The Order of Registration Matters](#-the-order-of-registration-matters)
- [🧠 Mnemonic Cheat Sheet](#-mnemonic-cheat-sheet)
- [🧪 Recall Test](#-recall-test)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 📖 The 30-Second Story

Yesterday your API had **one** URL (`/`). Today it has **three** (`/`, `/about`, `/users`). The only thing that changed: you added two more `@app.get(...)` decorators. That's the whole lesson — *FastAPI scales without restructuring*.

---

## 🎯 What You Will Learn (6 Skills)

| # | 🎯 Skill | 🧠 You'll remember it because... |
|:-:|:---------|:--------------------------------|
| 1 | 🛣️ Multiple routes per app | "Three phone numbers, one switchboard" |
| 2 | 🏷️ HTTP verbs | "POST = mail, GET = window-shopping" |
| 3 | 📤 Auto-JSON | "Return Python, get HTTP" |
| 4 | 🪪 Unique handler names | "Two functions with the same name = bug" |
| 5 | 📚 Swagger UI auto-lists all routes | "Visit `/docs` — it's all there" |
| 6 | 🔀 Route registration order | "Fixed paths before catch-alls" |

---

## 📂 Project Structure

```
📁 A003_Built_First_FastAPI/
├── 🐍 main.py     ← three routes, 20 lines
└── 📖 README.md   ← you are here
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

Visit <http://127.0.0.1:8000/docs> to see all three routes listed.

---

## 🧠 Anatomy of `main.py` — Line by Line

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
def about():                                    # ⚠️ same name as above!
    return {
        "users": ["Adnan", "umar", "Md"]
    }
```

### Line-by-line

| Line | Code | 🧠 Why it's there |
|:----:|:-----|:------------------|
| 1 | `from fastapi import FastAPI` | Framework import |
| 3 | `app = FastAPI()` | Single ASGI instance |
| 6–8 | `@app.get("/")` | The home route |
| 11–13 | `@app.get("/about")` | The about route |
| 16–20 | `@app.get("/users")` | The users route — *but the function is also named `about`* |

### 🎯 If you remember ONE thing
> **A route = one `@app.METHOD("/path")` decorator + one Python function.** That's the entire mental model.

---

## 🛣️ API Endpoints

| Method | Endpoint | Description | Sample Response |
|:------:|:---------|:------------|:----------------|
| 🟢 GET | `/` | Welcome message | `{"message": "Welcome to fastapi"}` |
| 🟢 GET | `/about` | About page | `{"message": "This is about page"}` |
| 🟢 GET | `/users` | Hard-coded user list | `{"users": ["Adnan", "umar", "Md"]}` |

---

## 🧪 Try It

### 🌐 Browser
```
http://127.0.0.1:8000/
http://127.0.0.1:8000/about
http://127.0.0.1:8000/users
```

### 💻 curl
```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/about
curl http://127.0.0.1:8000/users
```

### 🎨 Swagger UI
<http://127.0.0.1:8000/docs> — all three endpoints listed, clickable, runnable.

---

## 📐 HTTP & Routing Concepts

### The Five HTTP Verbs You'll Use 95% of the Time

| Verb | CRUD | Mnemonic | Real-world analogy |
|:-----|:----:|:---------|:--------------------|
| 🟢 `GET` | Read | "Gimme" | Window-shopping — read but don't touch |
| 🟡 `POST` | Create | "Postman" | Mailing a package to the server |
| 🟠 `PUT` | Update | "Put it back" | Editing your Amazon order |
| 🔴 `DELETE` | Delete | "Destroy" | Throwing something in the trash |
| 🟣 `PATCH` | Partial update | "Patch it" | Patching a tire — partial fix |

> 🧠 **Mnemonic: "G-P-P-D-P"** → **G**et, **P**ost, **P**ut, **D**elete, **P**atch.
> Story: **"Go, Please Pull Down, Pull up"**.

### What Each `@app.METHOD` Does Internally

```python
@app.get("/users")
def list_users():
    return {"users": [...]}
```

```
1. Request arrives:  GET /users
2. FastAPI matches "GET" + "/users" against registered routes
3. Calls the registered function (list_users)
4. Serializes return value to JSON
5. Adds headers: Content-Type: application/json
6. Sends HTTP 200 OK back
```

---

## ⚠️ Common Pitfalls & Fixes

### 🐛 Pitfall 1: Duplicate Function Names

In the code above, both `/about` and `/users` handlers are named `about`. Python silently **overwrites** the first definition with the second.

```python
def about():    # first definition
    return {...}

def about():    # second definition (same name!)
    return {...}    # ← Python keeps only THIS one
```

**Symptoms:**
- `/about` still works (uses the second `about`).
- `/users` returns the **about-page JSON**, not users!

**Rule:** Always give handler functions **unique names**, even if their URLs differ.

### 🐛 Pitfall 2: Trailing Slashes

```python
@app.get("/about")     # matches /about
@app.get("/about/")    # matches /about/  ← DIFFERENT route
```

By default FastAPI is strict. `/about/` ≠ `/about`. Pick one and stick with it.

### 🐛 Pitfall 3: Forgetting `--reload`

Without `--reload`, edits require manual Ctrl+C + restart.

### 🐛 Pitfall 4: Hard-Coded Data

Fine for learning. In production use a database.

---

## 🔧 Suggested Refactor

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

Notice the function names are now: `home`, `about_page`, `list_users` — **all unique**.

---

## 🧠 The Order of Registration Matters

```python
@app.get("/users/me")        # static path — registered FIRST
def read_me():
    return {"user_id": "me"}

@app.get("/users/{user_id}")  # dynamic — registered SECOND
def read_user(user_id: int):
    return {"user_id": user_id}
```

- `/users/me` → matches the static route.
- `/users/42` → falls through to the dynamic route.

> 🧠 **Mnemonic: "Specific before General"** — like a phone system: emergency numbers (specific) before auto-attendant (catch-all).

---

## 🧠 Mnemonic Cheat Sheet

| Concept | Mnemonic | Story |
|:--------|:---------|:------|
| HTTP verbs | **G-P-P-D-P** | "Go Please Pull Down, Pull up" |
| Route = | **URL + method → function** | "Phone number routing" |
| Handler names | **Unique names always** | "Two people named John = chaos" |
| Static vs dynamic | **Specific before general** | "Specific rooms before hallways" |

---

## 🧪 Recall Test

1. What's wrong with two handlers named `about`?
2. Name the five HTTP verbs you'll use most.
3. Why does the function name matter even if the URL is unique?
4. What's the difference between `/about` and `/about/`?
5. Which gets matched first: `/users/me` or `/users/{user_id}`?

> 5/5 → routing is yours.

---

## 🚀 Where to Go Next

| Direction | Module |
|:----------|:-------|
| ⬅️ Previous | [A002](../A002_FastAPI_Tutorial/) |
| ➡️ Next | [A004](../A004_Path_Parameter_Dynamic_Route_Validation/) — Path params |
| ⬅️ Back | [Root README](../README.md) |

---

<div align="center">

### 🛣️ *Three routes down. Dynamic routes coming up.* 🛣️

Made with ❤️ for FastAPI learners.

</div>