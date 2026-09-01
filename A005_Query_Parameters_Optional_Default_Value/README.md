<div align="center">

# 🔍 A005 — Query Parameters, Optional Values & Defaults

### *Filters, pagination & search — made easy*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Difficulty](https://img.shields.io/badge/Level-Beginner+-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Scaffold-orange?style=for-the-badge)
![Query](https://img.shields.io/badge/Query--Params-🔍-blueviolet?style=for-the-badge)

<br/>

> Query parameters are the optional key/value pairs after `?` in a URL — used for filtering, sorting, pagination, and search. This module is the **theory + scaffold** before you add the handlers.

</div>

---

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    🔍  /search?q=tea&limit=10&in_stock=true                   ║
║                                                               ║
║      q          = "tea"     → required string                 ║
║      limit      = 10        → optional, default 10            ║
║      in_stock   = true      → optional, default true          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 📑 Table of Contents

- [🎯 What You Will Learn](#-what-you-will-learn)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧠 Anatomy of main.py](#-anatomy-of-mainpy)
- [🧩 Theory — Query Parameters](#-theory--query-parameters)
- [🔧 Suggested Hands-On Code](#-suggested-hands-on-code)
- [🛣️ Recommended Endpoints](#-recommended-endpoints-to-add)
- [🧪 Testing Tools](#-testing-tools)
- [⚠️ Common Pitfalls](#-common-pitfalls)
- [📚 Further Reading](#-further-reading)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 🎯 What You Will Learn

| # | Skill | Description |
|:-:|:------|:------------|
| 1 | ❓ **Query Parameter** | What it is and how it differs from a path parameter. |
| 2 | ✍️ **Declaration Syntax** | `limit: int = 10` style. |
| 3 | 🔀 **Path vs Query** | How FastAPI decides what is what. |
| 4 | ⚙️ **Default Values** | Make a parameter optional. |
| 5 | 🧪 **Testing** | Browser + `curl` + Swagger UI. |

---

## 📂 Project Structure

```
📁 A005_Query_Parameters_Optional_Default_Value/
├── 🐍 main.py     # Empty FastAPI app — scaffold for query-parameter demos
└── 📖 README.md   # You are here
```

---

## ⚙️ Installation & Setup

```powershell
cd D:\AllProgram\LEARN\Python\FastAPI\A005_Query_Parameters_Optional_Default_Value
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "fastapi[standard]"
uvicorn main:app --reload
```

Visit <http://127.0.0.1:8000/docs> — Swagger UI is already live even with no routes defined.

---

## 🧠 Anatomy of `main.py`

```python
from fastapi import FastAPI

app = FastAPI()
```

That is the entire starter file. It deliberately contains **no routes** because the goal of this module is to:

1. 🏗️ Set up the project shell.
2. 📖 Explain the *theory* behind query parameters before writing handlers.
3. 🎨 Provide a clean canvas to add routes in the suggested exercises below.

---

## 🧩 Theory — Query Parameters

### 🌐 What is a Query String?

A URL such as

```
https://example.com/search?q=tea&limit=10&in_stock=true
```

consists of three parts:

| Part | Example | Meaning |
|:-----|:--------|:--------|
| 🛣️ **Path** | `/search` | The route of the resource. |
| ❓ **?** | `?` | Separator that introduces the query string. |
| 🔑 **Key** | `q`, `limit`, `in_stock` | Parameter names. |
| 🟰 **=** | `=` | Separates each key from its value. |
| 💎 **Value** | `tea`, `10`, `true` | Parameter values. |
| ➕ **&** | `&` | Separator between pairs. |

### 🆚 Path vs Query Parameters

| Feature | Path Parameter | Query Parameter |
|:--------|:---------------|:----------------|
| 📍 **Position** | Inside the URL path | After `?` in the URL |
| 🌐 **Example URL** | `/users/42` | `/users?id=42` |
| ❗ **Required by default** | Yes | No — but you can make them required |
| 🎯 **Common uses** | Identifying a *specific* resource | Filtering, sorting, pagination, search |
| 💡 **Type-hint effect** | Validates captured value | Validates provided value |

### 🤖 How FastAPI Knows It's a Query Parameter

FastAPI inspects the function signature and applies this rule:

> If a parameter name appears in the route path, it's a **path parameter**.
> Otherwise, it's a **query parameter** — provided it has a primitive type annotation (`int`, `str`, `bool`, …).

### ⚖️ Optional vs Required

| Declaration | Behavior |
|:------------|:---------|
| `def fn(q: str)` | ❗ **Required** — caller must supply `?q=...`. Otherwise `422`. |
| `def fn(q: str = "hello")` | ✅ **Optional** with default `"hello"`. |
| `def fn(q: str \| None = None)` | ✅ **Optional**, typed as `None` when absent. |
| `def fn(q: int = Query(10, ge=1))` | ✅ Optional default `10` but must be ≥ 1 if supplied. |

---

## 🔧 Suggested Hands-On Code

Try these in `main.py` while reading. Restart Uvicorn after each save (or rely on `--reload`).

### 1️⃣ The Simplest Query Parameter

```python
@app.get("/search")
def search(q: str):
    return {"query": q}
```

```bash
curl "http://127.0.0.1:8000/search?q=masala"
# {"query": "masala"}
```

### 2️⃣ Optional with Default Value

```python
@app.get("/items")
def list_items(limit: int = 10):
    return {"limit": limit}
```

```bash
curl "http://127.0.0.1:8000/items"          # {"limit": 10}
curl "http://127.0.0.1:8000/items?limit=5"  # {"limit": 5}
```

### 3️⃣ Multiple Query Parameters

```python
@app.get("/products")
def products(skip: int = 0, limit: int = 10, sort: str | None = None):
    return {"skip": skip, "limit": limit, "sort": sort}
```

```bash
curl "http://127.0.0.1:8000/products?skip=20&limit=5&sort=desc"
# {"skip": 20, "limit": 5, "sort": "desc"}
```

### 4️⃣ Required + Optional Mixed

```python
from fastapi import Query

@app.get("/users")
def get_users(role: str = Query(..., min_length=2),
              active: bool = True):
    return {"role": role, "active": active}
```

```bash
curl "http://127.0.0.1:8000/users?role=admin"
# {"role": "admin", "active": true}
```

### 5️⃣ Combining Path + Query

```python
@app.get("/users/{user_id}/orders")
def user_orders(user_id: int, status: str = "pending"):
    return {"user_id": user_id, "status": status}
```

```bash
curl "http://127.0.0.1:8000/users/42/orders?status=shipped"
# {"user_id": 42, "status": "shipped"}
```

---

## 🛣️ Recommended Endpoints to Add

| Method | Endpoint | Parameters | Purpose |
|:------:|:---------|:-----------|:--------|
| 🟢 **GET** | `/items` | `skip: int = 0`, `limit: int = 10` | Pagination basics |
| 🟢 **GET** | `/items/search` | `q: str`, `max_price: float \| None = None` | Filter by query and price |
| 🟢 **GET** | `/users/{user_id}/orders` | path: `user_id: int`, query: `status: str` | Mix path and query |
| 🟢 **GET** | `/products` | `category: str`, `in_stock: bool = True` | Boolean and string query handling |

---

## 🧪 Testing Tools

### 🌐 Browser

```
http://127.0.0.1:8000/items?limit=3
```

### 💻 `curl`

```bash
curl "http://127.0.0.1:8000/items?limit=3"
```

### 🎨 Swagger UI

Visit `/docs`, click an endpoint, hit **Try it out**, type a value, click **Execute**.

---

## ⚠️ Common Pitfalls

| 😖 Pitfall | ✅ Fix |
|:-----------|:------|
| 🔀 **Confusing path & query** | Declare the variable in the path *and* in the function signature. |
| ❗ **Forgetting default value** | `def fn(q: str)` is required; `def fn(q: str = "")` is optional. |
| ❌ **Wrong type** | Sending `?limit=abc` when the hint is `int` returns `422`. |
| 🏷️ **Naming clash** | `limit` shadows Python builtins in some libraries — prefer `limit` or `page_size`. |
| 🔣 **Special characters in URL** | URL-encode them (`%20` for space, etc.). |

---

## 📚 Further Reading

- 📘 Official tutorial — <https://fastapi.tiangolo.com/tutorial/query-params/>
- 📦 Query parameter models (Pydantic) — <https://fastapi.tiangolo.com/tutorial/query-param-models/>
- 🔀 Combining path + query + body — <https://fastapi.tiangolo.com/tutorial/body-multiple-params/>

---

## 🚀 Where to Go Next

| Next Module | Topic |
|:------------|:------|
| ⬅️ [`A004`](../A004_Path_Parameter_Dynamic_Route_Validation/) | Path parameters |
| ⬅️ [`A001`](../A001_CrashCourse/) | Full CRUD with Pydantic |
| 🚀 **A006 (upcoming)** | Request body + Pydantic |
| 🚀 **A007 (upcoming)** | Headers, cookies, and form data |

---

<div align="center">

### 🔍 *Filters added — now go compose path + query params in your own API!* 🔍

Made with ❤️ for FastAPI learners.

</div>