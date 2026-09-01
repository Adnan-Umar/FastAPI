# AGENTS.md

> Compact instructions for AI coding agents working in this FastAPI learning repository.
> Keep entries to facts an agent would otherwise miss or guess wrong.

---

## Repository at a glance

- **Type:** Personal FastAPI tutorial/lab. **Not** a deployable service, **no CI**, **no tests**, **no `pyproject.toml`**.
- **Layout:** Nine self-contained module folders (`A001_CrashCourse/` … `A009_Path_Query_Body_Together/`). Each is an *independent* mini-project with its own `main.py` (and optionally `README.md`, `requirements.txt`).
- **Stack:** Python 3.10+, FastAPI 0.141.x, Pydantic v2, Uvicorn. Only A001 has a pinned `requirements.txt`; the rest install via `pip install "fastapi[standard]"`.
- **Branch:** `main` (default). No protection rules, no PR template.

---

## How to run a module

Each folder is a standalone FastAPI app. From any module folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "fastapi[standard]"
uvicorn main:app --reload
```

Then open <http://127.0.0.1:8000/docs> for Swagger UI.

> 📝 The repo's `command.txt` (root) uses `py` instead of `python` for venv creation. Both work on Windows Python 3.10+. Prefer the explicit `python -m venv .venv` form in new scripts.

There is **no root-level `requirements.txt`** — each module that needs one has its own. Don't try to `pip install -r requirements.txt` at the repo root; it doesn't exist.

---

## Module entrypoints

| Folder | App entry | Notes |
|:-------|:----------|:------|
| A001 | `A001_CrashCourse/main.py` | Tea CRUD, in-memory list. Has `requirements.txt`. |
| A002 | `A002_FastAPI_Tutorial/main.py` | Single `GET /` returning JSON. |
| A003 | `A003_Built_First_FastAPI/main.py` | 3 GET routes. **Has a duplicate function name `about`** — see Gotchas. |
| A004 | `A004_Path_Parameter_Dynamic_Route_Validation/main.py` | `/users/{user_id}` with `int` validation. |
| A005 | `A005_Query_Parameters_Optional_Default_Value/main.py` | Query params: `/users`, `/products`, `/items`. |
| A006 | `A006_Request_Body_POST_API_Pydantic_Explained/main.py` | POST `/create-user` with `User` Pydantic model. |
| A007 | `A007_Pydanti_Models_Data_Validation_Nested_Schemas/main.py` | Nested `User → Address` model. |
| A008 | `A008_CRUD_API_TODO_App/main.py` | TODO CRUD (POST, GET-list, GET-by-id, PUT, DELETE). |
| A009 | `A009_Path_Query_Body_Together/main.py` | `PUT /users/{user_id}` combining **path + body + query** inputs. |

---

## Lint / format / typecheck

- **No linter, no formatter, no typechecker is configured.** No `ruff.toml`, no `mypy.ini`, no `pre-commit`.
- Do **not** invent or install one unless the user asks. Adding `ruff` to a tutorial repo surprises the user.
- No `tests/` directory and no test runner. Don't run `pytest` — it will fail with "no tests ran" or report collected errors.

---

## Repo conventions (verified)

- **Naming:** Folder names use a single `A0NN_<Topic>` prefix. Match this when adding a new module.
- **Per-folder `main.py`:** Always the FastAPI app. Keep it that way — don't introduce `app.py` or `server.py`.
- **Per-folder `README.md`:** All 9 existing modules (A001–A009) have a deep, memory-friendly README using mnemonics and a "If you remember ONE thing" section. **Match this style** if you add or update one.
- **Pinned versions:** A001 is the only folder with a `requirements.txt`. New modules can either omit it (use `fastapi[standard]`) or add one.

---

## Gotchas (worth preserving)

1. **A008 `main.py` is currently complete** (POST, GET-list, GET-by-id, PUT, DELETE all implemented). If the user reports it as broken, re-read the file before assuming it's truncated. Earlier versions *were* truncated; an edit since the original AGENTS.md was written restored the missing handlers.

2. **A002 / A003 originally had `READNE.md` (typo).** They were renamed to `README.md`. If you see `READNE.md` referenced anywhere (e.g. in old commits or new untracked code), rename it — do not create a second one.

3. **A003's `about` handlers share a name.** Both `/about` and `/users` route handlers are called `about` in the original code. This silently overwrites the first definition. The READMEs document this as a teaching moment. Don't "fix" it unless the user asks — it's intentional for the lesson.

4. **A009's update check is fragile.** The line `if user_id < len(users):` uses list length as if it were the max valid id. It breaks after deletes that leave gaps. The README documents this as a teaching moment. Don't "fix" it unless the user asks.

5. **In-memory storage everywhere.** All CRUD examples use a module-level Python list. Restarting the server wipes the data. Don't suggest adding SQLite/Postgres unless the user asks.

6. **`.gitignore` is set up.** `__pycache__/`, `.venv/`, `.env`, IDE folders, etc. are all ignored. Don't add them as tracked files.

7. **`uvicorn main:app --reload`** watches the **current directory's** `main.py`. If you `cd` to the repo root and run it, you'll get `ModuleNotFoundError`. Always `cd` into the module folder first.

---

## Files to avoid editing without asking

- `command.txt` — the user's personal cheat sheet, not a build script. Don't lint, format, or "fix" it.
- `README.md` (root) — the polished repo overview. Major changes should be confirmed.
- Individual module `main.py` files when the user only asks for a README update — they may be work-in-progress (see A008).

---

## Adding a new module (if the user asks)

1. Create `A00N_<Topic>/` (next number is 009).
2. Add `main.py` with a `FastAPI()` app.
3. Add a `README.md` matching the A001–A007 mnemonic style. Link back to the root `README.md` and to neighbours.
4. Do **not** commit `__pycache__/`, `.venv/`, or local files. `.gitignore` already excludes them.
5. Mention the new module in the root `README.md` module index table.

---

## Git workflow

- Single branch: `main`. Commits land directly; no PR flow.
- The user pushes manually after explicit instruction — do **not** auto-push.
- The user commits in clear logical units with imperative-mood messages. Match that style. Don't bundle unrelated changes.
- No tags, no releases, no changelog.

---

## What is NOT in this repo (don't assume it exists)

- ❌ `pyproject.toml`, `setup.py`, `setup.cfg`
- ❌ `pytest`, `unittest`, or any test framework
- ❌ GitHub Actions, `.github/workflows/`
- ❌ Pre-commit hooks, `.pre-commit-config.yaml`
- ❌ Docker, `Dockerfile`, `docker-compose.yml`
- ❌ Database drivers (SQLAlchemy, Tortoise, etc.)
- ❌ Authentication (OAuth2, JWT)
- ❌ Logging configuration
- ❌ Environment variable loading (no `pydantic-settings` usage)

If the user asks for any of these, treat it as a *new feature*, not as something to wire up to existing infrastructure.

---

## Quick reference — minimal agent context

If you only have 30 seconds:

- **9 independent FastAPI mini-projects** under `A001…A009/`.
- **One app per folder**, run with `uvicorn main:app --reload` from inside that folder.
- **No tests, no CI, no linter, no build system** — just `pip install "fastapi[standard]"` and go.
- **README style is mnemonic-heavy** — keep the style consistent.
- **A009's `user_id < len(users)` check is fragile** — don't try to "fix" without asking.
- **`.gitignore` exists** — don't add `__pycache__/`, `.venv/`, or IDE files.
