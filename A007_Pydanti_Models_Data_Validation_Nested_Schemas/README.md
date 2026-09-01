<div align="center">

# 🧬 A007 — Pydantic Models, Data Validation & Nested Schemas

### *When one model isn't enough — embed models inside models.*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Difficulty](https://img.shields.io/badge/Level-Intermediate-orange?style=for-the-badge)
![Reading Time](https://img.shields.io/badge/Read_Time-45_min-blueviolet?style=for-the-badge)
![Nested](https://img.shields.io/badge/Nested_Schemas-✅-success?style=for-the-badge)

</div>

---

## 🧠 The One-Sentence Summary

> **A Pydantic model is just a class with type-annotated fields; a *nested* model is one of those fields being another Pydantic class — and validation cascades through every layer automatically.**

If that sentence clicks, the rest of this README is just polish.

---

## 📑 Table of Contents

- [🧠 The One-Sentence Summary](#-the-one-sentence-summary)
- [📖 The Story: From Envelope to Parcel](#-the-story-from-envelope-to-parcel)
- [🎯 What You Will Learn (12 Skills)](#-what-you-will-learn-12-skills)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧬 Anatomy of `main.py` — Line by Line](#-anatomy-of-mainpy--line-by-line)
- [🛣️ API Endpoints](#-api-endpoints)
- [🧠 The Mental Model: Models Are Russian Dolls](#-the-mental-model-models-are-russian-dolls)
- [🔬 Deep Dive: What Makes Nested Models Special](#-deep-dive-what-makes-nested-models-special)
- [🧪 Try It With curl](#-try-it-with-curl)
- [❌ Failure Cases (422 Magic)](#-failure-cases-422-magic)
- [🔧 Variations You Should Know](#-variations-you-should-know)
- [🧠 Type Coercion vs Strict Mode](#-type-coercion-vs-strict-mode)
- [⚠️ Common Pitfalls & Fixes](#-common-pitfalls--fixes)
- [🧠 Mnemonic Cheat Sheet](#-mnemonic-cheat-sheet)
- [🧪 Recall Test](#-recall-test)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 📖 The Story: From Envelope to Parcel

In A006 you sent a **letter** (one `User` model). In the real world, people have **addresses**. An address has a city and a pincode. So your "letter" now contains a **smaller envelope inside**.

- ✉️ Outer envelope = `User`
- 📦 Inner envelope = `Address`
- 📝 Innermost = `city` (str), `pincode` (int)

Both envelopes get stamped and validated by Pydantic. Bad envelope inside? Whole letter rejected.

> 🧠 **Metaphor:** Nested models are **Russian dolls of validation** — every layer must pass.

---

## 🎯 What You Will Learn (12 Skills)

| # | 🎯 Skill | 🧠 You'll remember it because... |
|:-:|:---------|:--------------------------------|
| 1 | 🧬 **Define a Pydantic model** | "Class with type-annotated fields" |
| 2 | 🪆 **Nest a model in another** | "Address inside User" |
| 3 | 🛡️ **Cascading validation** | "Inner bad? Whole bad." |
| 4 | 📚 **Auto-generated JSON Schema** | "Swagger UI shows nested form" |
| 5 | 🔄 **Type coercion** | `"42"` → `42` automatically |
| 6 | 🛂 **Strict mode** | "Reject when types don't match exactly" |
| 7 | 📤 **model_dump()** | "Convert to plain Python dict" |
| 8 | 📦 **model_dump_json()** | "Convert to JSON string" |
| 9 | ⚙️ **Optional fields in nested models** | "Address.city required, Address.country optional" |
| 10 | 🏷️ **Field() constraints** | "min_length, ge, le, regex" |
| 11 | 🔁 **Lists of nested models** | "Multiple addresses per user" |
| 12 | 🆔 **response_model** | "Filter output by schema" |

---

## 📂 Project Structure

```
📁 A007_Pydanti_Models_Data_Validation_Nested_Schemas/
├── 🐍 main.py     ← flat → nested evolution + final code
└── 📖 README.md   ← you are here
```

> 💡 The `main.py` shows the **flat → nested** evolution. The first `User` (lines 7–17) is commented out; the **nested** version is active.

---

## ⚙️ Installation & Setup

```powershell
cd D:\AllProgram\LEARN\Python\FastAPI\A007_Pydanti_Models_Data_Validation_Nested_Schemas
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "fastapi[standard]"
uvicorn main:app --reload
```

Visit <http://127.0.0.1:8000/docs> — Swagger UI shows your nested `User → Address` schema as a form with collapsible sections.

---

## 🧬 Anatomy of `main.py` — Line by Line

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Flat schema (commented out — earlier attempt)
# class User(BaseModel):
#     name: str
#     age: int
#     email: str

class Address(BaseModel):
    city: str
    pincode: int

class User(BaseModel):
    name: str
    age: int
    address: Address             # ← nested model

@app.post("/create_user")
def create_user(user: User):
    return {
        "message": "User Created",
        "data": user
    }
```

| Line | Code | 🧠 Why it's there |
|:----:|:-----|:------------------|
| 1–2 | Imports | FastAPI + Pydantic |
| 4 | `app = FastAPI()` | App instance |
| 7–17 | *(commented)* Flat User | Earlier attempt — fine but limited |
| 19–21 | `class Address` | A model can be reused across the codebase |
| 24–27 | `class User` | Contains an `Address` as a field |
| 29–33 | `@app.post("/create_user")` | Accepts a `User`, returns it |

### The Three Pieces Every Model Needs

```python
class Address(BaseModel):
    city: str
    pincode: int
```

| Piece | What it does |
|:------|:-------------|
| `class Address(BaseModel)` | Inherit from `BaseModel` to get validation magic |
| `city: str` | Field with a type hint |
| `pincode: int` | Another field, integer validated |

> 🧠 **Mnemonic:** "**C-B-F-T**" — **C**lass, **B**aseModel, **F**ields, **T**ypes. (Class-BaseModel-Fields-Types)

---

## 🛣️ API Endpoints

| Method | Endpoint | Body | Returns |
|:------:|:---------|:-----|:--------|
| 🟡 POST | `/create_user` | `User` (with nested `Address`) | `{ message, data }` |

---

## 🧠 The Mental Model: Models Are Russian Dolls

```
┌─────────────────────────────────────────────┐
│  User (outer doll)                          │
│   ├── name: str                            │
│   ├── age: int                             │
│   └── address: Address (inner doll)        │
│           ├── city: str                    │
│           └── pincode: int                 │
│                                          │
│   Validation cascades:                     │
│     User invalid → 422                     │
│     Address invalid → 422                  │
│     pincode invalid → 422                  │
└─────────────────────────────────────────────┘
```

> 🧠 **Mnemonic:** "Outer first, inner deep" — like opening a Matryoshka doll, every layer must be checked.

### Why Nesting Matters in Real Apps

| Real-world concept | Single model | Nested model |
|:-------------------|:-------------|:-------------|
| User | name, age, **city**, **pincode** | name, age, **address: {city, pincode}** |
| Order | id, total, **product_name**, **price** | id, total, **items: [{name, price}]** |
| Company | name, **ceo_name**, **ceo_email** | name, **ceo: {name, email}** |

Nesting lets you **reuse** the inner model across many outer models:

```python
class Address(BaseModel):
    city: str
    pincode: int

class User(BaseModel):
    name: str
    address: Address

class Order(BaseModel):
    id: int
    shipping_address: Address     # ← same model, reused
```

---

## 🔬 Deep Dive: What Makes Nested Models Special

### 1️⃣ Validation cascades automatically

```python
# Outer valid, inner invalid → 422
{
  "name": "Adnan",
  "age": 25,
  "address": {"city": "Delhi", "pincode": "not-an-int"}
}
```

The error response **names the nested location**:

```json
{
  "detail": [{
    "type": "int_parsing",
    "loc": ["body", "address", "pincode"],   ← ← ← note the path!
    "msg": "Input should be a valid integer..."
  }]
}
```

> 🧠 **Mnemonic: "Path through the dolls"** — `loc` reads like a folder path: `body/address/pincode`.

### 2️⃣ Swagger UI renders nested forms

Open <http://127.0.0.1:8000/docs> and click **POST /create_user → Try it out**. You'll see a form with a collapsible `address` section that has its own `city` and `pincode` inputs.

### 3️⃣ Type coercion still works

```python
# Both work — Pydantic coerces string to int
{"name": "A", "age": "25", "address": {"city": "Delhi", "pincode": "110001"}}
{"name": "A", "age": 25,   "address": {"city": "Delhi", "pincode": 110001}}
```

### 4️⃣ Default factories — pre-fill nested data

```python
from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    city: str
    country: str = "India"            # ← default value
    pincode: Optional[int] = None     # ← optional
```

```json
// All three are valid:
{"city": "Delhi", "pincode": 110001}
{"city": "Delhi", "country": "USA", "pincode": 110001}
{"city": "Delhi", "country": "India", "pincode": null}
```

---

## 🧪 Try It With curl

### ✅ Success — flat nested

```bash
curl -X POST http://127.0.0.1:8000/create_user \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Adnan",
    "age": 25,
    "address": {
      "city": "Delhi",
      "pincode": 110001
    }
  }'
```

Response:

```json
{
  "message": "User Created",
  "data": {
    "name": "Adnan",
    "age": 25,
    "address": {
      "city": "Delhi",
      "pincode": 110001
    }
  }
}
```

### ✅ Success — string pincode (coerced)

```bash
curl -X POST http://127.0.0.1:8000/create_user \
  -H "Content-Type: application/json" \
  -d '{"name":"Md","age":"30","address":{"city":"Mumbai","pincode":"400001"}}'
```

Response: same shape, `pincode` becomes integer `400001`.

---

## ❌ Failure Cases (422 Magic)

### Missing nested field

```bash
curl -X POST http://127.0.0.1:8000/create_user \
  -H "Content-Type: application/json" \
  -d '{"name":"Adnan","age":25,"address":{"city":"Delhi"}}'
```

```json
{
  "detail": [{
      "type": "missing",
      "loc": ["body", "address", "pincode"],
      "msg": "Field required"
    }]
}
```

### Missing whole address

```bash
curl -X POST http://127.0.0.1:8000/create_user \
  -H "Content-Type: application/json" \
  -d '{"name":"Adnan","age":25}'
```

```json
{
  "detail": [{
      "type": "missing",
      "loc": ["body", "address"],
      "msg": "Field required"
    }]
}
```

### Wrong nested type

```bash
curl -X POST http://127.0.0.1:8000/create_user \
  -H "Content-Type: application/json" \
  -d '{"name":"Adnan","age":25,"address":{"city":"Delhi","pincode":"abc"}}'
```

```json
{
  "detail": [{
      "type": "int_parsing",
      "loc": ["body", "address", "pincode"],
      "msg": "Input should be a valid integer..."
    }]
}
```

> 🧠 **Mnemonic: "Path through the dolls"** — every nested error shows the full path in `loc`.

---

## 🔧 Variations You Should Know

### 1️⃣ List of nested models

```python
from typing import List

class Order(BaseModel):
    id: int
    items: List[Address]   # ← list of nested objects
```

```json
{
  "id": 1,
  "items": [
    {"city": "Delhi", "pincode": 110001},
    {"city": "Mumbai", "pincode": 400001}
  ]
}
```

### 2️⃣ Optional nested model

```python
from typing import Optional

class User(BaseModel):
    name: str
    age: int
    address: Optional[Address] = None    # ← entire address optional
```

```json
// All valid:
{"name":"Adnan","age":25,"address":{"city":"Delhi","pincode":110001}}
{"name":"Adnan","age":25,"address":null}
{"name":"Adnan","age":25}
```

### 3️⃣ Field constraints with `Field()`

```python
from pydantic import Field, BaseModel

class Address(BaseModel):
    city: str = Field(..., min_length=2, max_length=50)
    pincode: int = Field(..., ge=100000, le=999999)
```

| Argument | Meaning |
|:---------|:--------|
| `min_length` | String minimum length |
| `max_length` | String maximum length |
| `ge` | Greater than or equal (number) |
| `le` | Less than or equal (number) |
| `gt`, `lt` | Strictly greater / less |
| `regex` | Pattern match (use `pattern=` in v2) |
| `description` | Appears in Swagger docs |

### 4️⃣ model_dump() and model_dump_json()

```python
user = User(name="Adnan", age=25, address=Address(city="Delhi", pincode=110001))

# Convert to plain Python dict
user_dict = user.model_dump()
# {'name': 'Adnan', 'age': 25, 'address': {'city': 'Delhi', 'pincode': 110001}}

# Convert to JSON string
user_json = user.model_dump_json()
# '{"name":"Adnan","age":25,"address":{"city":"Delhi","pincode":110001}}'
```

> 🧠 **Mnemonic:** "**dump** = Python, **dump_json** = string."

### 5️⃣ Use the model as response_model

```python
@app.post("/create_user", response_model=User)
def create_user(user: User):
    return user
```

This tells FastAPI:
- ✅ Validate input as `User`
- ✅ Validate output as `User` (filters extra fields!)

### 🎯 If you remember ONE thing
> **Nested models are just Pydantic classes used as fields. Validation cascades through every layer.**

---

## 🧠 Type Coercion vs Strict Mode

By default, Pydantic **coerces** — converts `"42"` to `42`.

```python
class Address(BaseModel):
    pincode: int

Address(pincode="110001")    # ✅ coerced to 110001
```

In **strict mode**, types must match exactly:

```python
from pydantic import ConfigDict

class Address(BaseModel):
    model_config = ConfigDict(strict=True)
    pincode: int

Address(pincode="110001")    # ❌ ValidationError
Address(pincode=110001)      # ✅ OK
```

> 🧠 **Mnemonic:** "Coerce by default, strict on demand."

---

## ⚠️ Common Pitfalls & Fixes

| 😖 Pitfall | 🔍 Cause | ✅ Fix |
|:-----------|:---------|:------|
| Nested model arrives as `dict` instead of object | You forgot the type hint | Always annotate nested fields as the model class |
| Optional nested always required | `Optional[Address]` without `= None` | Add `= None` after the type |
| Want deeper validation | You used `dict` somewhere | Replace with a model |
| Field name vs alias mismatch | `pincode` in code, `pin_code` in JSON | Use `Field(alias="pin_code")` |
| Forgot to import `BaseModel` | SyntaxError | Always `from pydantic import BaseModel` |

---

## 🧠 Mnemonic Cheat Sheet

| Concept | Mnemonic | Story |
|:--------|:---------|:------|
| 3 model pieces | **C-B-F-T** | Class, BaseModel, Fields, Types |
| Nested = Russian dolls | "Outer first, inner deep" | Matryoshka validation |
| Error location | "Path through the dolls" | `body/address/pincode` |
| Coercion default | "Coerce by default, strict on demand" | Be lenient, then opt-in |
| Dump methods | "**dump** = Python, **dump_json** = string" | Two flavors |
| 422 = nested error | "Validation cascades" | Bad inner → whole bad |

---

## 🆕 Modern Patterns — Cross-field Validation & Generics

### Cross-field Validation with `@model_validator`

Sometimes a rule depends on **multiple fields** together:

```python
from pydantic import BaseModel, model_validator

class DateRange(BaseModel):
    start: str   # ISO date
    end: str

    @model_validator(mode="after")
    def check_order(self):
        if self.start > self.end:
            raise ValueError("start must be before end")
        return self
```

```bash
# ✅ Valid
{"start": "2026-01-01", "end": "2026-12-31"}

# ❌ 422 — model_validator catches it
{"start": "2026-12-31", "end": "2026-01-01"}
```

> 🧠 **Mnemonic:** "**@field_validator = one field. @model_validator = many fields.**"

### Generic Models (Pydantic v2)

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int

# Use it with any model
Page[User](items=[User(name="a", age=1)], total=1)
Page[Address](items=[Address(city="Delhi", pincode=110001)], total=1)
```

This is the same pattern FastAPI uses internally for `response_model=list[T]`.

### Annotated Nested Models

```python
from typing import Annotated
from pydantic import BaseModel, Field

class Address(BaseModel):
    city: Annotated[str, Field(min_length=2, max_length=50)]
    pincode: Annotated[int, Field(ge=100000, le=999999)]
```

Same constraints, modern syntax.

---

## 🧪 Recall Test

1. What's the syntax for a nested Pydantic model?
2. Where does a nested validation error show up in the 422 response?
3. How do you make a nested model optional?
4. What's the difference between `model_dump()` and `model_dump_json()`?
5. How do you constrain `pincode` to a 6-digit number?
6. What does `response_model=User` do?
7. How do you enable strict (no-coercion) mode?

> 7/7 → nested schemas are yours forever.

---

## 🚀 Where to Go Next

| Direction | Module |
|:----------|:-------|
| ⬅️ Previous | [A006](../A006_Request_Body_POST_API_Pydantic_Explained/) |
| ⬅️ Back | [Root README](../README.md) |
| ➡️ Next | A008 — Form Data, Files, Headers & Cookies |
| ➡️ Future | A009 — Response Models & Serialization |

---

<div align="center">

### 🧬 *"Models all the way down — validated at every layer."* 🧬

Made with ❤️ and a stack of nested envelopes.

---

## 🎯 Interview Q&A

### Q1: What is a nested Pydantic model?

**Answer:** A model that has another Pydantic class as one of its fields. Validation **cascades** through every layer.

```python
class Address(BaseModel):
    city: str
    pincode: int

class User(BaseModel):
    name: str
    address: Address    # ← nested
```

> **One-liner:** *"A model whose field is another model."*

### Q2: How does validation work for nested models?

**Answer:** Cascading — if the inner is bad, the outer fails. The 422 error's `loc` shows the path:

```json
{
  "detail": [{
    "type": "int_parsing",
    "loc": ["body", "address", "pincode"],
    ...
  }]
}
```

> **One-liner:** *"Validation cascades. The `loc` shows the path."*

### Q3: How do you make a nested field optional?

**Answer:** Use `Optional[T] = None`:

```python
class User(BaseModel):
    name: str
    address: Optional[Address] = None    # entire address optional
```

> **One-liner:** *"`Optional[Nested] = None` makes the whole block skippable."*

### Q4: How do you represent a list of nested objects?

**Answer:** Use `List[T]`:

```python
from typing import List

class Order(BaseModel):
    id: int
    items: List[Address]
```

```json
{
  "id": 1,
  "items": [
    {"city": "Delhi", "pincode": 110001},
    {"city": "Mumbai", "pincode": 400001}
  ]
}
```

> **One-liner:** *"`List[NestedModel]` = list of validated nested objects."*

### Q5: Why is "reusing" the nested model a best practice?

**Answer:** DRY (Don't Repeat Yourself). One `Address` model can be referenced by `User`, `Order`, `Company`, etc. — define once, validate everywhere.

> **One-liner:** *"Define once, reuse everywhere — DRY."*

### Q6: How do you switch Pydantic to strict mode (no type coercion)?

**Answer:** Add a `model_config` in v2:

```python
from pydantic import BaseModel, ConfigDict

class Address(BaseModel):
    model_config = ConfigDict(strict=True)
    pincode: int

Address(pincode="110001")    # ❌ ValidationError
Address(pincode=110001)      # ✅
```

> **One-liner:** *"Coerce by default, strict on demand."*

### Q7: What's the difference between `model_dump()` and `dict()` in Pydantic v2?

**Answer:** In Pydantic v2, the legacy `.dict()` is deprecated. Use:

| Method | Returns |
|:-------|:--------|
| `model_dump()` | Plain Python dict |
| `model_dump_json()` | JSON string |
| `model_dump(exclude_none=True)` | Dict without `None` fields |

> **One-liner:** *"`model_dump()` (v2) replaces `.dict()` (v1)."*

### Q8: How do you validate the response shape (not just the input)?

**Answer:** Use `response_model`:

```python
@app.post("/create_user", response_model=UserResponse)
def create_user(user: User): ...
```

FastAPI:
- ✅ Validates the return value
- ✅ Filters out extra fields
- ✅ Documents the response in `/docs`

> **One-liner:** *"`response_model` = input filter + output guard."*

</div>