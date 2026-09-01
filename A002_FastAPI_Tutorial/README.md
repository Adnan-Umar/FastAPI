<div align="center">

# 👋 A002 — FastAPI Tutorial

### *Your very first FastAPI "Hello World"!*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Difficulty](https://img.shields.io/badge/Level-Beginner-brightgreen?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-blue?style=for-the-badge)
![Endpoints](https://img.shields.io/badge/Endpoints-1-orange?style=for-the-badge)

<br/>

> The **simplest possible FastAPI application** — a single endpoint that returns a JSON message. Intentionally tiny so you can focus on the setup, project structure, and dev-server workflow.

</div>

---

```
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║    👋  Hello World from FastAPI venv                  ║
║                                                       ║
║    Routes:                                            ║
║      GET    /                                         ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
```

---

## 📑 Table of Contents

- [🎯 What You Will Learn](#-what-you-will-learn)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧠 Anatomy of main.py](#-anatomy-of-mainpy)
- [🛣️ API Endpoints](#-api-endpoints)
- [🧪 Try It](#-try-it)
- [⚠️ Common Pitfalls](#-common-pitfalls)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 🎯 What You Will Learn

| # | Skill | Description |
|:-:|:------|:------------|
| 1 | 📦 **Install** | Install FastAPI and Uvicorn in a clean project. |
| 2 | 🏗️ **App Instance** | Instantiate a FastAPI app. |
| 3 | 🛣️ **Register Route** | Use the `@app.get(...)` decorator. |
| 4 | 💡 **Type Hints** | Drive automatic JSON serialization. |
| 5 | 🔁 **Dev Server** | Launch with live-reload. |
| 6 | 📚 **Auto Docs** | Explore Swagger UI & ReDoc. |

---

## 📂 Project Structure

```
📁 A002_FastAPI_Tutorial/
├── 🐍 main.py     # The "Hello World" FastAPI app
└── 📖 README.md   # You are here
```

> 💡 There is **no** `requirements.txt` here on purpose — install dependencies manually using the commands below.

---

## ⚙️ Installation & Setup

### 📁 Step 1 — Move into the project

```powershell
cd D:\AllProgram\LEARN\Python\FastAPI\A002_FastAPI_Tutorial
```

### 🌿 Step 2 — Create a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 📥 Step 3 — Install FastAPI + Extras

```powershell
pip install "fastapi[standard]"
```

The `[standard]` extra installs:

| Package | Why |
|:--------|:----|
| ⚡ `fastapi` | The framework itself |
| 🚀 `uvicorn` | The ASGI server used to run the app |
| 🧪 `httpx` | Test client used by FastAPI's `TestClient` |
| 🎨 `jinja2` | Template engine (for HTML responses) |
| 📤 `python-multipart` | Required for form/file uploads |
| 📧 `email-validator` | Required for `EmailStr` validation |

### ▶️ Step 4 — Run the Dev Server

```powershell
uvicorn main:app --reload
```

You should see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

---

## 🧠 Anatomy of `main.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World from FastAPI venv"}
```

### 🔍 Line-by-Line Breakdown

| Line | Code | Explanation |
|:----:|:-----|:------------|
| 1 | `from fastapi import FastAPI` | Imports the framework's main class. |
| 3 | `app = FastAPI()` | Creates the ASGI application object. This is what Uvicorn serves. |
| 5 | `@app.get("/")` | Registers `home()` as the handler for HTTP `GET /`. |
| 6 | `def home():` | Plain synchronous Python function — FastAPI supports both `def` and `async def`. |
| 7 | `return {"message": ...}` | Returning a `dict` makes FastAPI serialize it to JSON automatically. |

> 💡 **Why does `def home()` work even though it returns a dict?**
> FastAPI inspects the return value, converts it to JSON, sets `Content-Type: application/json`, and returns `200 OK` — all without you writing any serialization code.

---

## 🛣️ API Endpoints

| Method | Endpoint | Description | Response |
|:------:|:---------|:------------|:---------|
| 🟢 **GET** | `/` | Returns a welcome message | `{ "message": "Hello World from FastAPI venv" }` |

---

## 🧪 Try It

### 🌐 Browser

Just open <http://127.0.0.1:8000/> in your browser. You should see:

```json
{
  "message": "Hello World from FastAPI venv"
}
```

### 💻 `curl`

```bash
curl http://127.0.0.1:8000/
```

### 📚 Auto-Generated Docs

| URL | What you get |
|:----|:-------------|
| <http://127.0.0.1:8000/docs> | 🎨 Interactive **Swagger UI** |
| <http://127.0.0.1:8000/redoc> | 📘 Clean reference **ReDoc** documentation |
| <http://127.0.0.1:8000/openapi.json> | 📄 Raw **OpenAPI 3.1** schema |

---

## ⚠️ Common Pitfalls

| 😖 Problem | ✅ Fix |
|:-----------|:------|
| `ModuleNotFoundError: No module named 'fastapi'` | Activate your virtual environment before running. |
| `Address already in use` | Another process is using port 8000. Run `uvicorn main:app --port 8001`. |
| Browser shows a blank page | You probably hit `/docs` or `/openapi.json`. The JSON lives at `/`. |
| Edited file but nothing changes | Make sure you used `--reload`. Stop and restart Uvicorn otherwise. |

---

## 🚀 Where to Go Next

| Next Module | Topic |
|:------------|:------|
| ⬅️ [`A001`](../A001_CrashCourse/) | Full CRUD with Pydantic |
| ➡️ [`A003`](../A003_Built_First_FastAPI/) | Building your first multi-route app |
| ➡️ [`A004`](../A004_Path_Parameter_Dynamic_Route_Validation/) | Path parameters and dynamic validation |
| ➡️ [`A005`](../A005_Query_Parameters_Optional_Default_Value/) | Optional query parameters and defaults |

---

<div align="center">

### 🚀 *Now that you've said "Hello" — let's add more routes in A003!* 🚀

Made with ❤️ for FastAPI learners.

</div>