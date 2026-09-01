<div align="center">

# ☕ A001 — FastAPI Crash Course

### *Build a complete Tea CRUD API in minutes!*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![CRUD](https://img.shields.io/badge/CRUD-Full-success?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Level-Beginner-brightgreen?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-blue?style=for-the-badge)

<br/>

> A complete, beginner-friendly crash course on FastAPI demonstrating all four CRUD operations with **Pydantic** validation.

</div>

---

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║    ☕  Welcome to Chai Code                                ║
║                                                           ║
║    Endpoints:                                             ║
║      GET    /                                             ║
║      GET    /teas                                         ║
║      POST   /teas                                         ║
║      PUT    /teas/{tea_id}                                ║
║      DELETE /teas/{tea_id}                                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 📑 Table of Contents

- [🎯 What You Will Learn](#-what-you-will-learn)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧠 Key Concepts](#-key-concepts-explained)
- [🛣️ API Endpoints](#-api-endpoints)
- [🧪 Try It With curl](#-try-it-with-curl)
- [🔍 Walk-through of main.py](#-walk-through-of-mainpy)
- [⚠️ Limitations](#-limitations-intentional)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 🎯 What You Will Learn

| # | Skill | Description |
|:-:|:------|:------------|
| 1 | 🏗️ **FastAPI Setup** | Install FastAPI, Uvicorn, and Pydantic in a virtual environment. |
| 2 | 🚀 **App Instance** | Create a `FastAPI()` application object. |
| 3 | 📦 **Pydantic Models** | Define a `BaseModel` subclass for automatic validation. |
| 4 | 🔄 **CRUD Routes** | Implement all four HTTP verbs: `GET`, `POST`, `PUT`, `DELETE`. |
| 5 | 💡 **Type Hints** | Let FastAPI auto-validate inputs and auto-generate docs. |
| 6 | 🎨 **Swagger UI** | Explore the interactive docs at `/docs`. |

---

## 📂 Project Structure

```
📁 A001_CrashCourse/
├── 🐍 main.py            # The entire FastAPI application
├── 📦 requirements.txt   # Pinned dependency versions
└── 📖 README.md          # You are here
```

| File | Purpose |
|:-----|:--------|
| `main.py` | Defines the FastAPI app, the `Tea` Pydantic model, and the CRUD routes. |
| `requirements.txt` | Reproducible install of all Python dependencies used in this module. |

---

## ⚙️ Installation & Setup

### 🔁 Step 1 — Create and Activate a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 📥 Step 2 — Install Dependencies

```powershell
pip install -r requirements.txt
```

<details>
<summary>📋 Click to view <code>requirements.txt</code> contents</summary>

```
annotated-doc==0.0.5
annotated-types==0.8.0
anyio==4.14.2
click==8.5.0
fastapi==0.141.1
h11==0.16.0
idna==3.19
pydantic==2.13.5
pydantic_core==2.46.5
starlette==1.6.0
typing-inspection==0.4.4
typing_extensions==4.16.0
uvicorn==0.52.4
```

</details>

### 🚀 Step 3 — Run the Server

```powershell
uvicorn main:app --reload
```

### 🌐 Step 4 — Open in Browser

| URL | Description |
|:----|:------------|
| <http://127.0.0.1:8000> | API root |
| <http://127.0.0.1:8000/docs> | 🎨 **Swagger UI** (interactive docs) |
| <http://127.0.0.1:8000/redoc> | 📘 **ReDoc** (reference docs) |
| <http://127.0.0.1:8000/openapi.json> | 📄 Raw OpenAPI 3.1 schema |

---

## 🧠 Key Concepts Explained

### 🏗️ 1. The FastAPI Application Instance

```python
from fastapi import FastAPI
app = FastAPI()
```

`app` is the main **ASGI** application object. Every route is registered on it with a decorator such as `@app.get("/")`.

### 📦 2. Pydantic Models — `Tea`

```python
from pydantic import BaseModel

class Tea(BaseModel):
    id: int
    name: str
    origin: str
```

> 🎁 **Free validation**: any incoming JSON body for a `Tea` is automatically parsed and validated. If a field is missing or the wrong type, FastAPI returns a **422 Unprocessable Entity** with a detailed error message — *you write zero validation code*.

### 💾 3. In-Memory Storage

```python
teas: List[Tea] = []
```

> ⚠️ The list acts as a tiny in-memory "database". **Restarting the server wipes all data** — perfect for learning, but use SQLite/PostgreSQL in production.

### 💡 4. Type Hints Drive Everything

| Annotation | What FastAPI Does |
|:-----------|:------------------|
| `id: int` | Validates & converts to integer |
| `name: str` | Validates string & length |
| `-> List[Tea]` | Generates response schema in docs |

---

## 🛣️ API Endpoints

Base URL: **`http://127.0.0.1:8000`**

| Method | Endpoint | Description | Body | Returns |
|:------:|:---------|:------------|:----:|:--------|
| 🟢 **GET**    | `/`              | Welcome message                | —     | `{ "message": "..." }` |
| 🟢 **GET**    | `/teas`          | List every tea in memory       | —     | `Tea[]`                |
| 🟡 **POST**   | `/teas`          | Add a new tea                  | `Tea` | Newly created `Tea`    |
| 🟠 **PUT**    | `/teas/{tea_id}` | Update an existing tea by ID   | `Tea` | Updated `Tea`          |
| 🔴 **DELETE** | `/teas/{tea_id}` | Delete a tea by ID             | —     | Deleted `Tea`          |

### 🟢 `GET /` — Welcome

```json
{ "message": "Welcome to chai code" }
```

### 🟢 `GET /teas`

```json
[]
```

### 🟡 `POST /teas` — Create

**Request body:**

```json
{
  "id": 1,
  "name": "Masala Chai",
  "origin": "India"
}
```

**Response:** the same object echoed back.

### 🟠 `PUT /teas/{tea_id}` — Update

```bash
PUT /teas/1
```

```json
{
  "id": 1,
  "name": "Kashmiri Kahwa",
  "origin": "Kashmir"
}
```

If the `tea_id` does not exist, the endpoint returns:

```json
{ "error": "Tea not found" }
```

### 🔴 `DELETE /teas/{tea_id}` — Delete

```bash
DELETE /teas/1
```

Returns the deleted tea, or an `error` key if the ID is unknown.

---

## 🧪 Try It With `curl`

```bash
# 🟡 Create
curl -X POST http://127.0.0.1:8000/teas \
  -H "Content-Type: application/json" \
  -d "{\"id\":1,\"name\":\"Masala Chai\",\"origin\":\"India\"}"

# 🟢 Read all
curl http://127.0.0.1:8000/teas

# 🟠 Update
curl -X PUT http://127.0.0.1:8000/teas/1 \
  -H "Content-Type: application/json" \
  -d "{\"id\":1,\"name\":\"Kashmiri Kahwa\",\"origin\":\"Kashmir\"}"

# 🔴 Delete
curl -X DELETE http://127.0.0.1:8000/teas/1
```

---

## 🔍 Walk-through of `main.py`

| Lines | Code Section | What It Does |
|:-----:|:-------------|:-------------|
| `1–3` | `from fastapi import FastAPI` etc. | Imports needed for the app and type hints. |
| `5` | `app = FastAPI()` | Creates the application instance. |
| `7–10` | `class Tea(BaseModel)` | Defines the schema for a tea. |
| `13` | `teas: List[Tea] = []` | In-memory "database". |
| `15–17` | `@app.get("/")` | Root route returns a welcome message. |
| `19–21` | `@app.get("/teas")` | Returns the entire list of teas. |
| `23–26` | `@app.post("/teas")` | Appends a new `Tea` and returns it. |
| `28–34` | `@app.put("/teas/{tea_id}")` | Iterates the list, replaces the matching tea, returns it. |
| `36–41` | `@app.delete("/teas/{tea_id}")` | Removes the matching tea and returns it. |

---

## ⚠️ Limitations (Intentional)

This is a *crash course* project. The following are **deliberately simplified** for clarity:

| # | Limitation | Why It's OK Here |
|:-:|:-----------|:-----------------|
| 1 | 💾 **No database** | Restarting the server clears all teas — perfect for learning. |
| 2 | 📊 **No status codes** | `POST` returns `200 OK`; ideally use `201 Created`. |
| 3 | ⏱️ **No async I/O** | Handlers are synchronous (`def`, not `async def`). |
| 4 | 🆔 **No duplicate handling** | Adding an existing `id` silently overwrites later lookups. |
| 5 | 🔓 **No authentication** | Anyone can call any endpoint. |

These limitations are intentionally left for the next modules to address.

---

## 🚀 Where to Go Next

| Next Module | Topic |
|:------------|:------|
| ➡️ [`A002`](../A002_FastAPI_Tutorial/) | Minimal "Hello World" FastAPI app |
| ➡️ [`A003`](../A003_Built_First_FastAPI/) | Building your first multi-route app |
| ➡️ [`A004`](../A004_Path_Parameter_Dynamic_Route_Validation/) | Path parameters and dynamic route validation |
| ➡️ [`A005`](../A005_Query_Parameters_Optional_Default_Value/) | Optional query parameters and default values |

---

<div align="center">

### 🌟 *If this helped you, star the repo and move on to A002!* 🌟

Made with ❤️ and ☕ for the FastAPI learning community.

</div>