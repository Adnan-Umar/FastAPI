📁 **Blog_API** — A complete FastAPI blog backend.

Implements a full **CRUD over Blog posts** (title + content) backed by a real database (SQLAlchemy + PostgreSQL in production, SQLite works locally), secured with **JWT authentication** on the write endpoints (`POST/PUT/DELETE /blogs`).

Built following the lessons in `A001` through `A023` — this is the **capstone integration** of everything.

<br/>

## ✨ What's inside

| File | Role |
|:-----|:-----|
| `main.py` | FastAPI app: CRUD routes + `GET /` + `POST /login` |
| `auth.py` | JWT token creation + verification (`python-jose`) |
| `config.py` | Loads `.env` → `Settings` singleton |
| `database.py` | SQLAlchemy `engine`, `SessionLocal`, `Base` |
| `models.py` | `Blog` ORM model |
| `schemas.py` | `BlogCreate` + `BlogResponse` Pydantic schemas |
| `.env` | Local secrets (git-ignored — **never commit yours**) |
| `requirements.txt` | Pinned dependencies |

---

## 🛠️ Quick start

```powershell
cd Blog_API
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Edit .env: set DB_URL to SQLite for a zero-setup local run
#   DB_URL="sqlite:///./blog.db"

uvicorn main:app --reload
```

Then open:

- <http://127.0.0.1:8000/docs> — Swagger UI

---

## 🛣️ API Endpoints

| Method | Endpoint | Auth | Body / Params | Returns |
|:------:|:---------|:----:|:--------------|:--------|
| 🟢 GET | `/` | none | — | `"Blog API Started"` |
| 🟡 POST | `/login` | none | — | `{access_token, token_type: "bearer"}` |
| 🟢 GET | `/blogs` | none | — | `[BlogResponse]` |
| 🟢 GET | `/blogs/{id}` | none | `id: int` | `BlogResponse` or 404 |
| 🔒 POST | `/blogs` | `Authorization: Bearer <token>` | `BlogCreate` JSON | `BlogResponse` |
| 🔒 PUT | `/blogs/{id}` | `Authorization: Bearer <token>` | `BlogCreate` JSON | `BlogResponse` or 404 |
| 🔒 DELETE | `/blogs/{id}` | `Authorization: Bearer <token>` | — | `{"message": "Blog deleted Successfully"}` |

> 🔒 = requires a valid JWT (`Authorization: Bearer <token>` header).

---

## 🔐 Auth flow

```
1. POST /login        →  {"access_token": "<jwt>", "token_type": "bearer"}
2. Use that token:
   POST /blogs  with  Authorization: Bearer <jwt>
3. Token verified by auth.verify_token
   via OAuth2PasswordBearer (Bearer scheme)
```

- Algorithm: `HS256`
- Token lifetime: `30` minutes (`ACCESS_TOKEN_EXPIRE_MINUTES`)
- Secret loaded from `SECRET_KEY` in `.env`

---

## 🗄️ Database

- **Engine**: SQLAlchemy `create_engine`
- **URL**: read from `DB_URL` in `.env` (default: PostgreSQL)
  - For local dev, use `DB_URL="sqlite:///./blog.db"`
- **Tables**: created on startup via `models.Base.metadata.create_all(bind=engine)`
- **Session**: a yield-based `get_db()` dependency (closes the session after each request)

---

## 🧪 Try it (curl)

```bash
# 1. Create a blog (no auth required to read, but write needs a token)
curl -X POST http://127.0.0.1:8000/login
# → {"access_token":"<jwt>","token_type":"bearer"}

# 2. Create a blog (with token)
curl -X POST http://127.0.0.1:8000/blogs \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"title":"My first post","content":"Hello world"}'

# 3. Read all blogs
curl http://127.0.0.1:8000/blogs
```

---

## ⚠️ Notes & gotchas

- The `/login` endpoint mints a token for `sub: "admin"` without a real user/password check — suitable for a demo, **not** for production. Use the password-hashing pattern from `A023` for real auth.
- `DB_URL` in `.env` is set to PostgreSQL by default. For local testing without Postgres, change it to `sqlite:///./blog.db`.
- `.env` is **git-ignored** (matched by `/.env` in the repo's `.gitignore`). A template `.env.example` is committed so new clones know which keys to set.
- The project is structurally separate from the numbered `A0xx` tutorial modules but reuses every concept from them.

---

## 🧠 Related modules

| Concept | This repo reuses | Tutorial module |
|:--------|:-----------------|:----------------|
| SQLAlchemy CRUD | `database.py`, `models.py`, `main.py` | A016–A020 |
| JWT auth | `auth.py` | A022, A023 |
| Pydantic schemas | `schemas.py` | A006, A007, A010 |
| `.env` config | `config.py` | A026 |
| CORS | add via `CORSMiddleware` in `main.py` | A025 |
