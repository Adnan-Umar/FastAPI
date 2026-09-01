<div align="center">

# 🔍 A005 — Query Parameters, Optional Values & Defaults

### *Filter, paginate, and search — without changing a single route.*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Difficulty](https://img.shields.io/badge/Level-Beginner+-yellow?style=for-the-badge)
![Reading Time](https://img.shields.io/badge/Read_Time-30_min-blueviolet?style=for-the-badge)
![Optional](https://img.shields.io/badge/Optional_by_Default-✅-success?style=for-the-badge)

</div>

---

## 🧠 The One-Sentence Summary

> **Anything in the URL after `?` is a query parameter; declare it as a normal Python parameter and FastAPI figures out the rest.**

If you remember *"after the `?` = optional, just declare it"*, the whole README is decoration.

---

## 📑 Table of Contents

- [🧠 The One-Sentence Summary](#-the-one-sentence-summary)
- [📖 The 30-Second Story](#-the-30-second-story)
- [🎯 What You Will Learn (8 Skills)](#-what-you-will-learn-8-skills)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧠 Anatomy of `main.py`](#-anatomy-of-mainpy)
- [🧩 Theory — Anatomy of a Query String](#-theory--anatomy-of-a-query-string)
- [🧠 The Four Forms of a Query Parameter](#-the-four-forms-of-a-query-parameter)
- [🛣️ Live Walk-through of the Current `main.py`](#-live-walk-through-of-the-current-mainpy)
- [🔧 Suggested Hands-On Code (5 Levels)](#-suggested-hands-on-code-5-levels)
- [🛣️ Recommended Endpoints to Add](#-recommended-endpoints-to-add)
- [🧪 Try It (4 Different Ways)](#-try-it-4-different-ways)
- [🧠 Path vs Query — When to Use Which](#-path-vs-query--when-to-use-which)
- [⚠️ Common Pitfalls & Fixes](#-common-pitfalls--fixes)
- [🧠 Mnemonic Cheat Sheet](#-mnemonic-cheat-sheet)
- [🧪 Recall Test](#-recall-test)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 📖 The 30-Second Story

Imagine a search box in Amazon. You type *"laptop"*, narrow by `brand=Dell`, sort by `price desc`. The URL grows: `?q=laptop&brand=Dell&sort=price_desc`. Each of those three key-value pairs is a **query parameter**.

In FastAPI you simply *declare them as function parameters*. No parsing, no validation glue. The framework does it all because — once again — **type hints are the contract**.

---

## 🎯 What You Will Learn (8 Skills)

| # | 🎯 Skill | 🧠 You'll remember it because... |
|:-:|:---------|:--------------------------------|
| 1 | ❓ What `?key=value` means | "Question mark = filter menu" |
| 2 | 📝 Declaration syntax | "Default value = optional" |
| 3 | ⚖️ Required vs optional | "No default = required" |
| 4 | 🔀 Multiple query params | "Comma-separated in URL, ordered in Python" |
| 5 | 💡 Type hints validate | "`int` = numbers only" |
| 6 | 🧰 `Query(...)` for metadata | "Add rules and descriptions" |
| 7 | 🔗 Combining path + query | "Identity from path, filter from query" |
| 8 | 🚫 `None` default pattern | "Pythonic optional pattern" |

---

## 📂 Project Structure

```
📁 A005_Query_Parameters_Optional_Default_Value/
├── 🐍 main.py     ← current code (see below)
└── 📖 README.md   ← you are here
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

---

## 🧠 Anatomy of `main.py`

```python
from fastapi import FastAPI

app = FastAPI()
```

The starter file is intentionally minimal — it teaches the *theory first*. The sections below give you 5 hands-on snippets to copy into `main.py`.

---

## 🧩 Theory — Anatomy of a Query String

```
https://example.com/search?q=tea&limit=10&in_stock=true
│                  │       │           │              │
│                  │       │           │              └─ value (true)
│                  │       │           └─ key (in_stock)
│                  │       └─ separator (&)
│                  └─ path (/search)
└─ host
```

| Symbol | Meaning |
|:------:|:--------|
| `?` | "Query string starts here" |
| `=` | "This key's value follows" |
| `&` | "Next parameter pair starts here" |

> 🧠 **Mnemonic:** *"Question, Equals, Ampersand"* → **Q**uery, **E**quals-value, **A**nd-next.

---

## 🧠 The Four Forms of a Query Parameter

### Form 1: **Required** — no default value

```python
@app.get("/search")
def search(q: str):
    return {"query": q}
```

| Request | Behavior |
|:--------|:---------|
| `GET /search?q=masala` | ✅ `{"query": "masala"}` |
| `GET /search` | ❌ 422 (q is missing) |

### Form 2: **Optional** with default value

```python
@app.get("/items")
def list_items(limit: int = 10):
    return {"limit": limit}
```

| Request | Behavior |
|:--------|:---------|
| `GET /items` | ✅ `{"limit": 10}` (default) |
| `GET /items?limit=5` | ✅ `{"limit": 5}` (overridden) |

### Form 3: **Optional** with `None`

```python
@app.get("/products")
def products(sort: str | None = None):
    return {"sort": sort}
```

| Request | Behavior |
|:--------|:---------|
| `GET /products` | ✅ `{"sort": null}` |
| `GET /products?sort=desc` | ✅ `{"sort": "desc"}` |

### Form 4: **Required** with metadata via `Query(...)`

```python
from fastapi import Query

@app.get("/users")
def get_users(role: str = Query(..., min_length=2),
              active: bool = True):
    return {"role": role, "active": active}
```

| Request | Behavior |
|:--------|:---------|
| `GET /users?role=admin` | ✅ `{"role": "admin", "active": true}` |
| `GET /users` | ❌ 422 (role missing) |

> 🧠 **`...` (three dots) means REQUIRED.** Same as Python's `Ellipsis`.

### 🎯 If you remember ONE thing
> **Default value = optional. No default = required. Type hint = validator.**

---

## 🛣️ Live Walk-through of the Current `main.py`

Your `main.py` currently contains:

```python
from fastapi import FastAPI

app = FastAPI()
```

It returns:

| URL | Response |
|:----|:---------|
| `/` | ❌ 404 Not Found |
| `/docs` | ✅ Swagger UI (empty endpoint list) |
| `/redoc` | ✅ ReDoc |

> Even an empty app gives you `/docs` and `/redoc`. Add routes and they appear there.

---

## 🔧 Suggested Hands-On Code (5 Levels)

> 🧠 **Mnemonic:** "**ROMEO**" — **R**equired, **O**ptional-default, **M**ultiple, **E**xtra-metadata, **O**bject-mix.

### Level 1: One Required Query

```python
@app.get("/search")
def search(q: str):
    return {"query": q}
```

```bash
curl "http://127.0.0.1:8000/search?q=masala"
# {"query":"masala"}
```

### Level 2: One Optional with Default

```python
@app.get("/items")
def list_items(limit: int = 10):
    return {"limit": limit}
```

```bash
curl "http://127.0.0.1:8000/items"          # {"limit":10}
curl "http://127.0.0.1:8000/items?limit=5"  # {"limit":5}
```

### Level 3: Multiple Optional

```python
@app.get("/products")
def products(skip: int = 0, limit: int = 10, sort: str | None = None):
    return {"skip": skip, "limit": limit, "sort": sort}
```

```bash
curl "http://127.0.0.1:8000/products?skip=20&limit=5&sort=desc"
# {"skip":20,"limit":5,"sort":"desc"}
```

### Level 4: Required + Metadata

```python
from fastapi import Query

@app.get("/users")
def get_users(role: str = Query(..., min_length=2),
              active: bool = True):
    return {"role": role, "active": active}
```

```bash
curl "http://127.0.0.1:8000/users?role=admin"
# {"role":"admin","active":true}
```

### Level 5: Path + Query Combined

```python
@app.get("/users/{user_id}/orders")
def user_orders(user_id: int, status: str = "pending"):
    return {"user_id": user_id, "status": status}
```

```bash
curl "http://127.0.0.1:8000/users/42/orders?status=shipped"
# {"user_id":42,"status":"shipped"}
```

---

## 🛣️ Recommended Endpoints to Add

| Method | Endpoint | Parameters | Purpose |
|:------:|:---------|:-----------|:--------|
| 🟢 GET | `/items` | `skip: int = 0`, `limit: int = 10` | Pagination basics |
| 🟢 GET | `/items/search` | `q: str`, `max_price: float \| None = None` | Filter by query + price |
| 🟢 GET | `/users/{user_id}/orders` | path: `user_id: int`, query: `status: str` | Mix path + query |
| 🟢 GET | `/products` | `category: str`, `in_stock: bool = True` | Booleans + strings |

---

## 🧪 Try It (4 Different Ways)

### 🌐 Browser
```
http://127.0.0.1:8000/items?limit=3
```

### 💻 curl
```bash
curl "http://127.0.0.1:8000/items?limit=3"
```

### 🧪 Python `httpx`
```python
import httpx
r = httpx.get("http://127.0.0.1:8000/items", params={"limit": 3})
print(r.json())
```

### 🎨 Swagger UI
Visit `/docs`, click an endpoint, **Try it out**, fill the form, click **Execute**.

---

## 🧠 Path vs Query — When to Use Which

| Use case | Path parameter | Query parameter |
|:---------|:---------------|:----------------|
| Identifying *one* resource | ✅ `/users/42` | ❌ |
| Filtering a list | ❌ | ✅ `/users?active=true` |
| Pagination | ❌ | ✅ `/items?skip=20&limit=10` |
| Sorting | ❌ | ✅ `/products?sort=price` |
| Resource hierarchy | ✅ `/users/42/orders/7` | ❌ |
| Optional flags | ❌ | ✅ `/export?format=pdf` |

> 🧠 **Mnemonic: "Path = Identity, Query = Modifier"** — the path tells you *which* resource, the query tells you *how to shape* it.

---

## ⚠️ Common Pitfalls & Fixes

| 😖 Pitfall | 🔍 Cause | ✅ Fix |
|:-----------|:---------|:------|
| 422 on `/items` (no params) | Parameter has no default | Add `= 10` (or similar) |
| Query param ignored | You named it differently than the URL | Match the URL key to the Python name |
| `?limit=abc` returns 422 | Type hint is `int` | Either change hint to `str` or send a number |
| Same param, two values | URL has `?tag=a&tag=b` | Use `tag: list[str] = Query([])` |
| `bool` default ambiguity | `?active=false` is string `"false"` | FastAPI parses it; just trust it |

### Multiple Values for One Parameter

```python
from fastapi import Query
from typing import List

@app.get("/search")
def search(tags: List[str] = Query([])):
    return {"tags": tags}
```

```bash
GET /search?tags=tea&tags=coffee
# {"tags": ["tea", "coffee"]}
```

---

## 🧠 Mnemonic Cheat Sheet

| Concept | Mnemonic | Story |
|:--------|:---------|:------|
| Anatomy of query string | "QEA" | Question, Equals, Ampersand |
| 4 forms of query | "ROMEO" | Required, Optional-default, Multiple, Extra-metadata, Object-mix |
| `Query(...)` | "Three dots = required" | Like Python's Ellipsis |
| Path vs Query | "Identity vs Modifier" | Path tells which, query tells how |
| Multiple values | `list[T] = Query([])` | "Square brackets = empty list default" |

---

## 🆕 Modern Style — `Annotated` Syntax

> Recommended for **new code**. Cleaner, more composable, and easier to read.

### The Old vs New

```python
# Legacy (still works)
def list_items(limit: int = Query(10, ge=1, le=100)): ...

# Modern (recommended)
from typing import Annotated
from fastapi import Query

def list_items(limit: Annotated[int, Query(ge=1, le=100)] = 10): ...
```

| Aspect | Legacy | Modern `Annotated` |
|:-------|:-------|:-------------------|
| Default lives in | `Query()` | After `=` |
| Reuse the same constraint | Copy/paste `Query(...)` | Define a type alias |
| Editor type-checking | Sometimes confused | Clean |
| FastAPI version | All | 0.95+ |

### Reusable Type Aliases — the Killer Feature

```python
from typing import Annotated
from fastapi import Query

# Define ONCE
PositiveInt = Annotated[int, Query(ge=1, le=10_000)]

# Reuse EVERYWHERE
@app.get("/users/{user_id}")
def get_user(user_id: PositiveInt): ...

@app.get("/orders/{order_id}")
def get_order(order_id: PositiveInt): ...
```

Same constraint, two endpoints, zero duplication.

> 🧠 **Mnemonic:** "**Annotated = meta-data sandwich**" — the type is the bread, the metadata is the filling.

---

## 🧪 Recall Test

1. What's the difference between `?key=val` and `/key/val`?
2. What makes a query parameter optional in FastAPI?
3. What does `Query(...)` mean?
4. Which is for identity: path or query?
5. How do you allow multiple values for one query key?
6. What status code does FastAPI return on missing required query?

> 6/6 → query parameters are yours forever.

---

## 🚀 Where to Go Next

| Direction | Module |
|:----------|:-------|
| ⬅️ Previous | [A004](../A004_Path_Parameter_Dynamic_Route_Validation/) |
| ⬅️ Back | [Root README](../README.md) |
| 🚀 A006 (upcoming) | Request Body + Pydantic |
| 🚀 A007 (upcoming) | Headers, Cookies, Form data |

---

<div align="center">

### 🔍 *"After the `?`, anything goes."* 🔍

Made with ❤️ for FastAPI learners.

---

## 🎯 Interview Q&A

### Q1: What is a query parameter?

**Answer:** A **key=value** pair that appears in the URL after `?`, separated by `&`. They are typically used for filtering, sorting, pagination, and search.

```
https://example.com/search?q=tea&limit=10
                       │         │
                       path      query
```

> **One-liner:** *"After the `?` = filter menu."*

### Q2: How does FastAPI know a function parameter is a query parameter?

**Answer:** **By elimination.** If a parameter:

1. Does NOT appear in the route path's `{}` slots → it's a query param
2. IS a Pydantic model → it's a body param
3. Matches `{name}` in the path → it's a path param

```python
@app.get("/items")
def list(limit: int = 10): ...    # limit → query (default 10)
```

> **One-liner:** *"Not in path + not a model = query."*

### Q3: How do you make a query parameter required?

**Answer:** **No default value.**

```python
@app.get("/search")
def search(q: str): ...          # required
def search(q: str = ""): ...     # optional
def search(q: str | None = None):  # optional, None default
```

Or use `Query(...)` for explicit metadata:

```python
from fastapi import Query

def search(q: str = Query(..., min_length=2)): ...   # required
```

> **One-liner:** *"No default = required. `Query(...)` is explicit."*

### Q4: How do you accept multiple values for one query key?

**Answer:** Use a `List` type:

```python
from typing import List
from fastapi import Query

@app.get("/filter")
def filter_tags(tags: List[str] = Query([])):
    return tags
```

```bash
GET /filter?tags=tea&tags=coffee&tags=chai
# → ["tea", "coffee", "chai"]
```

> **One-liner:** *"`List[T] = Query([])` accepts multiple values."*

### Q5: What's the difference between path and query parameters in code?

**Answer:**

| Path | Query |
|:-----|:------|
| In the URL path | After `?` |
| Captured automatically | Declared as parameter |
| Required by default | Optional by default |
| Identifies a resource | Modifies the response |

In code:

```python
@app.get("/users/{user_id}/orders")
def get_orders(user_id: int, status: str = "pending"): ...
#              ^path             ^path  ^query
```

> **One-liner:** *"Path identifies, query filters."*

### Q6: How do you add metadata to a query parameter?

**Answer:** Use `Query()`:

```python
from fastapi import Query

@app.get("/users")
def get_users(
    role: str = Query(..., min_length=2, max_length=20, description="User role"),
    active: bool = True
):
    ...
```

This shows up in `/docs` and adds validation rules.

> **One-liner:** *"`Query(...)` adds metadata + validation."*

### Q7: How do you type a query param that accepts any string?

**Answer:** Just use `str`. To accept anything (string-coercible), use `str` with no constraints. For numeric, use `int` / `float`. For booleans, FastAPI parses `"true"`, `"false"`, `"1"`, `"0"`.

> **One-liner:** *"Type the param. FastAPI parses it."*

### Q8: Can query parameters have nested or complex types?

**Answer:** Yes — use a Pydantic model via `Depends()`:

```python
from fastapi import Depends
from pydantic import BaseModel

class Filter(BaseModel):
    skip: int = 0
    limit: int = 10
    sort: str | None = None

@app.get("/items")
def list_items(filter: Filter = Depends()):
    return filter
```

This is called a **query parameter model**.

> **One-liner:** *"Use a Pydantic model + `Depends()` for complex query shapes."*

</div>