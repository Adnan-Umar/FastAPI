<div align="center">

# 🔐 A026 — Environment Variables (.env + python-dotenv)

### *Move secrets and config out of the code. Put them in a `.env` file.*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![python-dotenv](https://img.shields.io/badge/python--dotenv-1.0.1-blue?style=for-the-badge)
![12-factor](https://img.shields.io/badge/12--Factor-Config-success?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Level-Beginner%2B-blue?style=for-the-badge)
![Reading Time](https://img.shields.io/badge/Read_Time-45_min-blueviolet?style=for-the-badge)

</div>

---

## 🧠 The One-Sentence Summary

> **Put secrets and per-environment values in a `.env` file, load them once with `python-dotenv` at startup, and access them through a `Settings` object — never hard-code `SECRET_KEY` or `DB_URL` in your source.**

If you remember *"**L-P-S** — **L**oad `.env` once, **P**arse, expose via **S**ettings"*, the rest of this README is decoration.

---

## 📑 Table of Contents

- [🧠 The One-Sentence Summary](#-the-one-sentence-summary)
- [📖 The Story: The Restaurant's Order Ticket](#-the-story-the-restaurants-order-ticket)
- [🎯 What You Will Learn (10 Skills)](#-what-you-will-learn-10-skills)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧬 Anatomy of `main.py` — Line by Line (Heavily Commented)](#-anatomy-of-mainpy--line-by-line-heavily-commented)
- [🧬 Anatomy of `config.py` — Line by Line (Heavily Commented)](#-anatomy-of-configpy--line-by-line-heavily-commented)
- [🛣️ API Endpoints](#-api-endpoints)
- [🧠 The Mental Model: Where Config Lives](#-the-mental-model-where-config-lives)
- [🆕 Every New Keyword Explained](#-every-new-keyword-explained)
- [🆚 Hard-coded vs .env vs OS env vs Vault](#-hard-coded-vs-env-vs-os-env-vs-vault)
- [🧪 Try It](#-try-it)
- [🔧 Variations](#-variations)
- [⚠️ Common Pitfalls & Fixes](#-common-pitfalls--fixes)
- [🧠 Mnemonic Cheat Sheet](#-mnemonic-cheat-sheet)
- [🧪 Recall Test](#-recall-test)
- [🎯 Interview Q&A](#-interview-qa)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 📖 The Story: The Restaurant's Order Ticket 🍽️

Imagine a chef who keeps recipes **written on the kitchen wall**:

| Where the recipe lives | Problem |
|:------------------------|:--------|
| 📜 Pinned to the wall (hard-coded) | Every branch uses the same wall; can't change per location |
| 🗒️ On a note the manager swaps in (`.env`) | Branch A uses one note; Branch B uses another; no rebuild needed |
| ☁️ In a corporate vault (Vault / AWS SSM) | Even more secure; rotated automatically |

> 🧠 **Mnemonic:** "**Wall = code. Note = `.env`. Vault = secret manager.**"

---

## 🎯 What You Will Learn (10 Skills)

| # | 🎯 Skill | 🧠 You'll remember it because... |
|:-:|:---------|:--------------------------------|
| 1 | 📜 **What a `.env` file is** | "`KEY=VALUE` per line" |
| 2 | 📥 **`load_dotenv()`** | "Loads .env into `os.environ`" |
| 3 | 🔍 **`os.getenv("KEY")`** | "Read a single env var" |
| 4 | 🗂️ **The `Settings` pattern** | "One object, many attrs" |
| 5 | 📋 **JSON lists in env** | "ORIGINS=`['http://a', 'http://b']`" |
| 6 | 🚫 **`.env` in `.gitignore`** | "Never commit secrets" |
| 7 | 📑 **`.env.example`** | "Commit this, ignore the real one" |
| 8 | 🥇 **Env > real env vars** | "Don't use `override=True`" |
| 9 | 🔐 **`pydantic-settings`** | "Future-proof upgrade" |
| 10 | 🪤 **Exposing secrets in responses** | "Don't print `SECRET_KEY` in JSON" |

---

## 📂 Project Structure

```
📁 A026_Environment_Variables_env_Setup_python_dotenv/
├── 🐍 main.py                       ← FastAPI app + CORS from settings
├── ⚙️ config.py                     ← Settings class (loads .env)
├── 📄 .env                          ← ACTUAL secrets — git-ignored
├── 📑 .env.example                  ← template — tracked in git
├── 📦 requirements.txt              ← fastapi[standard] + python-dotenv
└── 📖 README.md                     ← you are here
```

> 🧠 **`.env` is your real config (with secrets). `.env.example` is the template you commit.**

---

## ⚙️ Installation & Setup

```powershell
cd "D:\AllProgram\LEARN\Python\FastAPI\A026_Environment_Variables_env_Setup_python_dotenv"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env    # one-time; then edit .env
uvicorn main:app --reload
```

Then open <http://127.0.0.1:8000/docs>.

> 🧠 **The repo's `.gitignore` already excludes `.env` files** (`/.env`, `/.env.*`), so your real secrets will not be committed.

---

## 🧬 Anatomy of `main.py` — Line by Line (Heavily Commented)

```python
# --- FastAPI: framework + CORS middleware ---
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- Local config module (loads .env at import time) ---
from config import settings

# 1. Create the FastAPI app instance
app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)


# =========================================================
# CORS — origins come from the .env file, not hard-coded
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,    # list[str] parsed by config.py
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# Health check
# =========================================================
@app.get("/")
def home():
    return {
        "message": f"{settings.APP_NAME} running",
        "debug": settings.DEBUG,
    }


# =========================================================
# Config inspector — show NON-SENSITIVE settings
# =========================================================
# ⚠️  Never return the raw SECRET_KEY or DB credentials here.
#     This endpoint shows what's safe to expose (app name, origins,
#     a boolean saying whether a SECRET_KEY is configured, etc.)
@app.get("/config")
def get_config():
    return {
        "app_name": settings.APP_NAME,
        "debug": settings.DEBUG,
        "origins": settings.origins,
        "has_secret_key": bool(settings.SECRET_KEY),    # boolean only
        "db_url_scheme": (settings.DB_URL or "").split("://", 1)[0],
    }
```

| Line | Code | 🧠 Why it's there |
|:----:|:-----|:------------------|
| 6 | `from config import settings` | Import the singleton |
| 8 | `app = FastAPI(title=settings.APP_NAME, ...)` | Use config in app metadata |
| 18 | `allow_origins=settings.origins` | CORS list from `.env` |
| 32 | `has_secret_key: bool(...)` | Boolean, **not the secret itself** |
| 33 | `db_url_scheme: ...split("://")[0]` | Only the scheme (`sqlite`), not the path/creds |

### 🎯 If you remember ONE thing
> **`.env` holds secrets. `python-dotenv` loads it. `Settings` exposes it. Never echo `SECRET_KEY` in a response.**

---

## 🧬 Anatomy of `config.py` — Line by Line (Heavily Commented)

```python
from dotenv import load_dotenv
import os

load_dotenv()    # one-time: read .env into os.environ


def _parse_list(raw: str | None) -> list[str]:
    """Accept JSON list or comma-separated string."""
    if not raw:
        return []
    raw = raw.strip()
    if raw.startswith("["):
        import json
        return json.loads(raw)             # ORIGINS=["a", "b"]
    return [s.strip() for s in raw.split(",") if s.strip()]    # ORIGINS=a,b


class Settings:
    def __init__(self) -> None:
        self.origins     = _parse_list(os.getenv("ORIGINS"))
        self.SECRET_KEY  = os.getenv("SECRET_KEY")
        self.DB_URL      = os.getenv("DB_URL")
        self.APP_NAME    = os.getenv("APP_NAME", "FastAPI App")
        self.DEBUG       = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")


settings = Settings()    # singleton
```

| Section | Code | 🧠 Why it's there |
|:--------|:-----|:------------------|
| `load_dotenv()` | one-time at import | Merges `.env` into `os.environ` |
| `_parse_list()` | JSON or CSV parser | Env vars are always strings |
| `class Settings` | One object, many attrs | Clean import surface |
| `__init__` | Reads each var with default | Per-key fallback values |
| `settings = Settings()` | Singleton | `from config import settings` anywhere |

---

## 🛣️ API Endpoints

| Method | Endpoint | Returns |
|:------:|:---------|:--------|
| 🟢 GET | `/` | `{message, debug}` (uses `APP_NAME` and `DEBUG`) |
| 🟢 GET | `/config` | Non-sensitive config view (no real `SECRET_KEY`) |

> ⚠️ **`/config` deliberately hides the secret value.** It returns `has_secret_key: true/false` instead.

---

## 🧠 The Mental Model: Where Config Lives

```
┌────────────────────────────────────────────────────┐
│  your code                                        │
│   from config import settings                     │
│   print(settings.SECRET_KEY)                      │
└──────────────┬─────────────────────────────────────┘
               │ import
               ▼
┌────────────────────────────────────────────────────┐
│  config.py                                        │
│   load_dotenv()                                   │
│   class Settings: ...                             │
│   settings = Settings()                           │
└──────────────┬─────────────────────────────────────┘
               │ reads
               ▼
┌────────────────────────────────────────────────────┐
│  os.environ   ←   load_dotenv() merges .env here  │
│                    (without overriding real env)  │
└──────────────┬─────────────────────────────────────┘
               │ merged from
               ▼
┌────────────────────────────────────────────────────┐
│  .env (git-ignored)                               │
│   SECRET_KEY=...                                  │
│   ORIGINS=[...]                                   │
│   DB_URL=sqlite:///./test.db                      │
└────────────────────────────────────────────────────┘
```

> 🧠 **`.env` is the lowest-priority source.** Real env vars (set in the shell, by Docker, by the cloud) take precedence.

---

## 🆕 Every New Keyword Explained

### 1. `.env` file

**What:** A plain-text file in the project root, one `KEY=VALUE` per line. Used to keep secrets out of source control.

```ini
SECRET_KEY=mysecret
ORIGINS=["http://localhost"]
DB_URL=sqlite:///./test.db
```

> 🧠 **Mnemonic:** "**`.env` = `KEY=VALUE` per line.**"

### 2. `python-dotenv` (the package)

**What:** A library that reads a `.env` file and merges its values into `os.environ`. Provides `load_dotenv()` and `dotenv_values()`.

```bash
pip install python-dotenv
```

> 🧠 **Mnemonic:** "**`python-dotenv` = the loader.**"

### 3. `load_dotenv()`

**What:** Reads `.env` from the current working directory and merges into `os.environ`. **Does not override** existing env vars (by default).

```python
from dotenv import load_dotenv
load_dotenv()             # safe to call once at startup
```

| Flag | Behavior |
|:-----|:---------|
| `load_dotenv()` | `.env` only fills in MISSING env vars |
| `load_dotenv(override=True)` | `.env` always wins (use carefully) |
| `load_dotenv(dotenv_path="...")` | Load a specific file |

> 🧠 **Mnemonic:** "**`load_dotenv` = 'fill the gaps, don't fight real env'**."

### 4. `os.getenv("KEY", default)`

**What:** Read an env var, returning the default if it's missing. **Always returns a `str`** (or `None` if no default given).

```python
db = os.getenv("DB_URL", "sqlite:///./default.db")
debug = os.getenv("DEBUG", "false")
```

> 🧠 **Mnemonic:** "**`os.getenv` = 'give me the string, or the default'**."

### 5. `os.environ["KEY"]`

**What:** Read an env var; raises `KeyError` if missing. Use this when you **require** the value to be set.

```python
SECRET_KEY = os.environ["SECRET_KEY"]    # crashes if not set
```

> 🧠 **Mnemonic:** "**`os.environ` is dict-style; `os.getenv` is forgiving.**"

### 6. `Settings` class

**What:** A plain Python class (or `pydantic-settings.BaseSettings`) that holds the config for your app. Import it as a singleton.

```python
class Settings:
    origins = _parse_list(os.getenv("ORIGINS"))
    SECRET_KEY = os.getenv("SECRET_KEY")

settings = Settings()
```

> 🧠 **Mnemonic:** "**`Settings` = one object, many keys.**"

### 7. `.env.example`

**What:** A tracked-in-git template file that lists every key your app reads, with placeholder values. New developers copy it to `.env` and fill in their own values.

```ini
# .env.example
SECRET_KEY=change-me
ORIGINS=["http://localhost:3000"]
```

> 🧠 **Mnemonic:** "**`.env.example` is the recipe; `.env` is the cooked dish.**"

### 8. `pydantic-settings`

**What:** The production-grade upgrade to the plain `Settings` class. It validates types (int, bool, list, datetime), reads `.env` automatically, and gives nice error messages.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    SECRET_KEY: str
    ORIGINS: list[str] = []
    DEBUG: bool = False

settings = Settings()
```

> 🧠 **Mnemonic:** "**`pydantic-settings` = typed + validated config.**"

### 9. 12-Factor App — Config

**What:** A widely-adopted methodology that says: **store config in the environment, not in the code**. That's the whole reason `.env` files exist.

> 🧠 **Mnemonic:** "**Config in env, not in code.**"

### 10. Secret manager (Vault, AWS SSM, etc.)

**What:** A service that stores secrets centrally, rotates them, and hands them to your app at runtime. The `.env` pattern is fine for small apps; production usually graduates to a secret manager.

> 🧠 **Mnemonic:** "**`.env` for dev. Vault for prod.**"

---

## 🆚 Hard-coded vs .env vs OS env vs Vault

| Where config lives | Pros | Cons | Use for |
|:-------------------|:-----|:-----|:--------|
| Hard-coded in `main.py` | Trivial | Secrets in git, no per-env override | 🚫 Demos only |
| `.env` file | Per-dev overrides, git-ignored | File can leak; no rotation | ✅ Dev, small apps |
| OS env vars (`export FOO=bar`) | Works everywhere; no file | Hard to manage across services | ✅ Containers, CI |
| `.env` + real env override | `.env` for defaults, real env wins | Slightly more complex | ✅ Production-ish |
| Vault / AWS SSM / GCP SM | Encrypted at rest, rotation, audit | Extra infra | ✅ Enterprise |

> 🧠 **Mnemonic:** "**Code → .env → OS env → Vault. Each level is more secure than the last.**"

---

## 🧪 Try It

### 1. Inspect the `.env`

```ini
SECRET_KEY="mysecretkey123"
ORIGINS=["http://localhost", "http://localhost:8000"]
DB_URL=sqlite:///./test.db
APP_NAME=A026 Demo API
DEBUG=true
```

### 2. Start the server

```powershell
uvicorn main:app --reload
```

### 3. Hit `/` and `/config`

```bash
curl http://127.0.0.1:8000/
# {"message":"A026 Demo API running","debug":true}

curl http://127.0.0.1:8000/config
# {
#   "app_name": "A026 Demo API",
#   "debug": true,
#   "origins": ["http://localhost", "http://localhost:8000"],
#   "has_secret_key": true,
#   "db_url_scheme": "sqlite"
# }
```

Notice: **no raw `SECRET_KEY` is exposed.**

### 4. Override via OS env (wins over `.env`)

```powershell
$env:APP_NAME = "Overridden via PowerShell"
$env:DEBUG = "false"
uvicorn main:app --reload
```

```bash
curl http://127.0.0.1:8000/
# {"message":"Overridden via PowerShell running","debug":false}
```

### 5. Edit `.env` to add a new value

```ini
ORIGINS=["http://localhost", "http://localhost:8000", "http://example.com"]
```

Reload (uvicorn auto-reloads). Hit `/config` — the new origin appears.

---

## 🔧 Variations

### Variation 1: Use `pydantic-settings` (typed config)

```python
# pip install pydantic-settings
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    SECRET_KEY: str                              # required
    ORIGINS: list[str] = []                      # default []
    DEBUG: bool = False
    DB_URL: str = "sqlite:///./default.db"

settings = Settings()    # validates types; raises on bad values
```

### Variation 2: Comma-separated origins (no JSON)

```ini
ORIGINS=http://localhost,http://localhost:8000,http://example.com
```

`config.py`'s `_parse_list` already handles this format.

### Variation 3: Type-cast booleans

```python
def _bool(s: str | None) -> bool:
    return (s or "").lower() in ("1", "true", "yes", "on")

settings.DEBUG = _bool(os.getenv("DEBUG"))
```

### Variation 4: Nested env vars (e.g. `DATABASE__HOST`)

```python
class Settings(BaseSettings):
    DATABASE__HOST: str = "localhost"
    DATABASE__PORT: int = 5432
```

`pydantic-settings` maps `DATABASE__HOST` to `settings.DATABASE__HOST` automatically (note: `__` becomes a nested attribute).

### Variation 5: Load multiple env files

```python
load_dotenv(".env")                 # defaults
load_dotenv(".env.local", override=True)    # per-developer overrides
```

`.env.local` is git-ignored and is the common "my laptop's database password" pattern.

---

## ⚠️ Common Pitfalls & Fixes

| 😖 Pitfall | 🔍 Cause | ✅ Fix |
|:-----------|:---------|:------|
| `KeyError: 'SECRET_KEY'` | `os.environ[...]` and the key isn't set | Use `os.getenv` with a default, or fail loudly at startup |
| `.env` changes ignored | You forgot to restart the server | Restart `uvicorn` (or use `--reload`) |
| `origins` is a string, not a list | `os.getenv` returns a string | Parse JSON or split on `,` |
| `CORS: allow_origins must be a list` | Passed a string to `allow_origins` | Always parse to `list[str]` in `config.py` |
| Secret leaked to git | `.env` not in `.gitignore` | Add `/.env`, `/.env.*` to `.gitignore` (already in this repo) |
| `pydantic-settings` complains about types | Env value doesn't match type | Cast in env (`DEBUG=true`) or use `Optional[...]` with a default |
| Empty list of origins | `ORIGINS` not set in `.env` | Provide a default in `_parse_list` (returns `[]`) |
| Different `SECRET_KEY` per developer | `.env` should differ per machine | `.env` is git-ignored — each dev has their own |
| `load_dotenv()` from a different directory | CWD is not the project root | Pass `dotenv_path=os.path.join(os.path.dirname(__file__), ".env")` |

### The "Secret in Response" Trap

```python
# ❌ Echoes the secret to anyone who calls the endpoint
@app.get("/config")
def get_config():
    return {"secret": settings.SECRET_KEY}

# ✅ Boolean only; never the value
@app.get("/config")
def get_config():
    return {"has_secret_key": bool(settings.SECRET_KEY)}
```

### The "Loaded the Wrong File" Trap

```python
# ❌ CWD is `D:\Some\Other\Folder`; load_dotenv looks there
load_dotenv()

# ✅ Always load from a known location
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
```

### The "String Where a List Was Expected" Trap

```ini
# ❌ This is a string: "['http://a', 'http://b']"
ORIGINS=["http://localhost"]
```

```python
# CORSMiddleware expects a list — passing a string crashes
allow_origins=os.getenv("ORIGINS")    # ← string, not list
```

```python
# ✅ Parse in config.py
self.origins = _parse_list(os.getenv("ORIGINS"))    # list[str]
```

> 🧠 **Mnemonic:** "**Env vars are strings. Parse them before using.**"

---

## 🧠 Mnemonic Cheat Sheet

| Concept | Mnemonic | Story |
|:--------|:---------|:------|
| 3-step flow | **L-P-S** | Load, Parse, Settings |
| `.env` | `KEY=VALUE` per line | Git-ignored |
| `python-dotenv` | The loader | Reads `.env` into `os.environ` |
| `load_dotenv()` | Fills the gaps | Real env wins by default |
| `os.getenv("KEY", default)` | Forgiving read | Returns `str` or default |
| `os.environ["KEY"]` | Strict read | Raises `KeyError` |
| `Settings` class | One object, many attrs | Singleton |
| `.env.example` | The recipe | Track in git |
| `pydantic-settings` | Typed upgrade | Validates + reads .env |
| 12-Factor | Config in env | Not in code |
| Vault | For production | Rotates + encrypts |
| CORS list from env | Parse to list | Env vars are strings |

---

## 🧪 Recall Test

1. What is a `.env` file?
2. How do you load it in Python?
3. What's the difference between `os.getenv` and `os.environ`?
4. Why should you commit `.env.example` but not `.env`?
5. How do you handle a JSON list in an env var?
6. Why is exposing `SECRET_KEY` in a `/config` endpoint a bad idea?
7. How do you override a `.env` value with a real env var?
8. What's the production-grade upgrade to a plain `Settings` class?

> 8/8 → env vars are yours.

---

## 🎯 Interview Q&A

### Q1: What is a `.env` file and why use it?

**Answer:** A plain-text file in the project root, one `KEY=VALUE` per line. Used to keep secrets and per-environment config out of source code. `.env` is added to `.gitignore`; `.env.example` (the template) is tracked.

> **One-liner:** *"`KEY=VALUE` per line. Git-ignored. Per-machine."*

### Q2: How do you load a `.env` file in Python?

**Answer:** Use `python-dotenv`:

```python
from dotenv import load_dotenv
load_dotenv()             # merges .env into os.environ
```

By default it doesn't override existing env vars, so OS / container / cloud env wins.

> **One-liner:** *"`load_dotenv()` fills the gaps."*

### Q3: What's the difference between `os.getenv` and `os.environ`?

**Answer:**

| `os.getenv("KEY", default)` | `os.environ["KEY"]` |
|:-----------------------------|:---------------------|
| Returns the value, or `default`/`None` | Raises `KeyError` if missing |
| Forgiving, lazy | Strict, eager |

> **One-liner:** *"`getenv` is forgiving; `environ` is strict."*

### Q4: Why should you commit `.env.example` but not `.env`?

**Answer:** `.env` contains **real secrets** for one machine (DB password, JWT key). Committing it leaks those to anyone with repo access. `.env.example` is a **template** with placeholder values — committing it tells new developers "these are the keys you need to set" without leaking anything.

> **One-liner:** *"Commit the recipe, not the dish."*

### Q5: How do you handle a JSON list in an env var?

**Answer:** Parse it in your config layer:

```python
import json
def _parse_list(raw):
    if raw and raw.strip().startswith("["):
        return json.loads(raw)
    return [s.strip() for s in (raw or "").split(",") if s.strip()]

settings.origins = _parse_list(os.getenv("ORIGINS"))
```

Env vars are always strings; libraries like `CORSMiddleware` need actual lists.

> **One-liner:** *"Env vars are strings. Parse them."*

### Q6: Why is exposing `SECRET_KEY` in a `/config` endpoint a bad idea?

**Answer:** Any client can call the endpoint and read the JWT signing key. They can then mint their own valid tokens and impersonate any user. Always return a **boolean** ("is a secret configured?") or a **non-sensitive** summary ("the DB scheme is sqlite"), never the raw secret.

> **One-liner:** *"Never echo secrets in responses."*

### Q7: How do you override a `.env` value with a real env var?

**Answer:** By default, `load_dotenv()` **does not override** existing env vars. So:

```powershell
$env:APP_NAME = "Production App"
uvicorn main:app
```

`settings.APP_NAME` will be `"Production App"`, not whatever's in `.env`. To force `.env` to win, use `load_dotenv(override=True)` — but this is rarely what you want.

> **One-liner:** *"Real env wins by default. `.env` is the fallback."*

### Q8: What's the production-grade upgrade to a plain `Settings` class?

**Answer:** `pydantic-settings.BaseSettings`:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    SECRET_KEY: str
    ORIGINS: list[str] = []
    DEBUG: bool = False

settings = Settings()    # type-checked; bad values raise
```

It validates types, reads `.env` automatically, and gives clear error messages on bad input. For multi-service prod apps, use a real secret manager (Vault, AWS SSM) and feed the values to `pydantic-settings` via OS env.

> **One-liner:** *"`pydantic-settings` = typed + validated + reads .env."*

---

## 🚀 Where to Go Next

| Direction | Module |
|:----------|:-------|
| ⬅️ Previous | [A025](../A025_CORS_Explained_Connect_React_with_FastAPI/) |
| ⬅️ Back | [Root README](../README.md) |
| ➡️ Next | A027 (planned) — `pydantic-settings` typed config |
| ➡️ Future | A028 (planned) — Docker + env files for deploys |

---

<div align="center">

### 🔐 *Secrets in `.env`. `.env` in `.gitignore`. Real env wins.* 🔐

Made with ❤️, `load_dotenv()`, and `os.getenv("KEY")`.

</div>