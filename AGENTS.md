# AGENTS.md

> Compact instructions for AI coding agents working in this FastAPI learning repository.
> Keep entries to facts an agent would otherwise miss or guess wrong.

---

## Repository at a glance

- **Type:** Personal FastAPI tutorial/lab. **Not** a deployable service, **no CI**, **no tests**, **no `pyproject.toml``.
- **Layout:** Thirty self-contained module folders (`A001_CrashCourse/` … `A030_Pagination_Explained_Limit_Real_API_Example/`). Each is an *independent* mini-project with its own `main.py` (and optionally `README.md`, `requirements.txt`).
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
| A010 | `A010_Response_Models_Data_Validation_Hide_Sensitive_Data/main.py` | `response_model=UserResponse` filters out `password` from a `User` return. |
| A011 | `A011_Status_Codes_Custom_Responses_Error_Handling/main.py` | Status codes (`201`), custom `{status, message, data}` responses, and `HTTPException` for `404`. |
| A012 | `A012_Exception_Handling_HTTPException_Global_Error_Handler/main.py` | Custom `UserNotFoundException` + `@app.exception_handler(...)` for a centralized 404 response. |
| A013 | `A013_Dependency_Injection_Depends()_Auth_Example/main.py` | `verify_token` dep + `@app.get("/secure-data", user=Depends(verify_token))` — token check via `Header`. |
| A014 | `A014_Middleware_Explained_Logging_Request_Response_Flow/main.py` | `@app.middleware("http")` with `await call_next(request)` for request/response timing and logging. |
| A015 | `A015_SQLite_Database_Integration_Setup_SQLAlchemy_Intro/main.py` | Raw `sqlite3` connect + cursor + `CREATE TABLE`. **Folder name says SQLAlchemy but `main.py` uses raw `sqlite3`** — note the mismatch. |
| A016 | `A016_SQLAlchemy_Setup_Models_Database_Integration/main.py` | SQLAlchemy ORM: `create_engine` + `sessionmaker` + `declarative_base` + `Todo` model + `get_db` yield dependency. **Requires `pip install sqlalchemy`** (not in `fastapi[standard]`). |
| A017 | `A017_CREATE_Operation_with_Database/main.py` | `POST /todos` with `db.add → db.commit → db.refresh` pattern. **`title` is taken as a query param, not a JSON body** (not idiomatic; see README for the Pydantic-body fix). |
| A018 | `A018_READ_Operation_with_Database/main.py` | `GET /todos` (list) + `GET /todos/{id}` (one) with `db.query(Todo).all()` and `.filter(...).first()`. **Throws 404 on missing id.** |
| A019 | `A019_UPDATE_Operation_with_Database/main.py` | `PUT /todos/{todo_id}` — query, mutate `todo.title`, `db.commit()`. **Throws 404 on missing id.** |
| A020 | `A020_DELETE_Operation_with_Database/main.py` | `DELETE /todos/{todo_id}` — query, `db.delete(todo)`, `db.commit()`. **Throws 404 on missing id.** |
| A021 | `A021_Async_Await_Explained_Async_Programming/main.py` | `GET /` as `async def` with `await asyncio.sleep(3)` — demonstrates non-blocking yield to the event loop. |
| A022 | `A022_JWT_Authentication_Token_Based_Auth_Login_API/main.py` | `POST /login` issues a JWT (`python-jose` HS256); `GET /secure` gated by `Depends(verify_token)`. 401 on invalid/expired. **Requires `pip install python-jose[cryptography]`.** |
| A023 | `A023_OAuth2_JWT_Authentication_Secure_Routes_Password_Hashing/main.py` | `POST /login` with `OAuth2PasswordRequestForm` (form body), `passlib` hashed passwords, `OAuth2PasswordBearer` for `Authorization: Bearer …`. **Requires `pip install python-jose[cryptography] passlib`.** |
| A024 | `A024_File_Upload_Serve_Static_Files_(Images_PDFs)/main.py` | `POST /upload` (multipart) + `StaticFiles` mount at `/files/<filename>`; extension whitelist + path-traversal guard. **Requires `pip install python-multipart` (bundled in `fastapi[standard]`).** |
| A025 | `A025_CORS_Explained_Connect_React_with_FastAPI/main.py` | `CORSMiddleware` allowing `http://localhost:5173`; `GET /`, `GET /todos`, `POST /todos`. Paired with a Vite + React 18 frontend in `frontend/`. |
| A026 | `A026_Environment_Variables_env_Setup_python_dotenv/main.py` | `Settings` class loading `.env` via `python-dotenv`; CORS origins + JWT secret + DB URL from env; non-sensitive `/config` endpoint. **Requires `pip install python-dotenv`.** |
| A027 | `A027_API_Testing_with_Pytest_FastAPI_Test_Endpoints/main.py` | `TestClient(app)` + `pytest`; tests `GET /` and `GET /add`. **Requires `pip install pytest httpx`.** |
| A028 | `A028_Third_Party_API_Integration_Requests_Library_Fetch_External_Data/main.py` | Proxy routes (`GET /posts`, `GET /posts/{post_id}`) that call `jsonplaceholder` via `requests`; translates upstream errors into `HTTPException`s. **Requires `pip install requests`.** |
| A029 | `A029_Web_Crawling_Requests_BeautifulSoup_Fetch_Website_Data/main.py` | `GET /news` fetches `indianexpress.com` via `requests`, parses with `BeautifulSoup`, extracts headlines with `find_all`. **Requires `pip install requests beautifulsoup4`.** |
| A030 | `A030_Pagination_Explained_Limit_Real_API_Example/main.py` | `GET /news` crawls `news.ycombinator.com`, extracts titles, slices with `page`/`limit` query params. Returns `{page, limit, total, data}`. **Requires `pip install requests beautifulsoup4`.** |

---

## Lint / format / typecheck

- **No linter, no formatter, no typechecker is configured.** No `ruff.toml`, no `mypy.ini`, no `pre-commit`.
- Do **not** invent or install one unless the user asks. Adding `ruff` to a tutorial repo surprises the user.
- No `tests/` directory and no test runner. Don't run `pytest` — it will fail with "no tests ran" or report collected errors.

---

## Repo conventions (verified)

- **Naming:** Folder names use a single `A0NN_<Topic>` prefix. Match this when adding a new module.
- **Per-folder `main.py`:** Always the FastAPI app. Keep it that way — don't introduce `app.py` or `server.py`.
- **Per-folder `README.md`:** All 30 existing modules (A001–A030) have a deep, memory-friendly README using mnemonics, a "If you remember ONE thing" section, and an "Interview Q&A" section (8 questions per module). **Match this style** if you add or update one.
- **Interview Q&A convention:** Every module README ends with an `## 🎯 Interview Q&A` section containing **8 questions** (one per common interview topic for that module). Each answer follows the pattern: short prose answer + comparison table where useful + a "One-liner" summary. If you add a new module, write 8 Q&A items in the same style.
- **Diagrams:** ASCII art and Mermaid diagrams are encouraged wherever a flow, hierarchy, or sequence helps comprehension. They are first-class content, not decoration.
- **Theory depth:** READMEs must be **deeply detailed** — cover minor topics, edge cases, and gotchas in full, not just the happy path. The user values thoroughness over brevity. Add comparison tables, error/edge-case examples, and "what's happening under the hood" walkthroughs wherever they apply. Don't summarize when you can explain.
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

- **30 independent FastAPI mini-projects** under `A001…A030/`.
- **One app per folder**, run with `uvicorn main:app --reload` from inside that folder.
- **No tests, no CI, no linter, no build system** — just `pip install "fastapi[standard]"` and go.
- **README style is mnemonic-heavy** — keep the style consistent.
- **A009's `user_id < len(users)` check is fragile** — don't try to "fix" without asking.
- **`.gitignore` exists** — don't add `__pycache__/`, `.venv/`, or IDE files.
