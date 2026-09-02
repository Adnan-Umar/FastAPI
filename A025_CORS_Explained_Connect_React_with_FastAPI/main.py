# =========================================================
# A025 — CORS Explained (Connect React with FastAPI)
# =========================================================
# What this module demonstrates:
#   - The browser's Same-Origin Policy blocks cross-origin requests
#     (e.g. React at http://localhost:5173 calling FastAPI at
#     http://127.0.0.1:8000)
#   - CORS (Cross-Origin Resource Sharing) is the server's way of
#     saying "yes, I trust requests from this origin"
#   - We use FastAPI's CORSMiddleware to allow specific origins
# =========================================================

# --- FastAPI: framework + CORS middleware ---
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. Create the FastAPI app instance (Uvicorn serves THIS object)
app = FastAPI()


# =========================================================
# STEP 1 — Define the allowed origins
# =========================================================
# An "origin" = scheme + host + port.
#   http://localhost:5173/   ← Vite (default dev port)
#   http://127.0.0.1:5173/   ← Vite (alt)
#   http://localhost:3000/   ← Create React App (legacy)
#
# ⚠️  Note the trailing slash: "http://localhost:5173/" is technically
# different from "http://localhost:5173". Browsers ignore the trailing
# slash on the path, but be consistent in your list.
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]


# =========================================================
# STEP 2 — Add the CORS middleware
# =========================================================
# The middleware wraps every response. When the browser sees a
# cross-origin request, it sends a "preflight" OPTIONS request first;
# CORSMiddleware answers with the right Access-Control-* headers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,        # which origins may call us
    allow_credentials=True,               # allow cookies / Authorization headers
    allow_methods=["*"],                  # GET, POST, PUT, DELETE, PATCH, OPTIONS
    allow_headers=["*"],                  # Content-Type, Authorization, X-*, ...
)


# =========================================================
# SAMPLE ROUTES
# =========================================================
# A plain JSON response the React app can fetch
@app.get("/")
def home():
    return {
        "message": "CORS Enabled API",
        "cors_origins": ALLOWED_ORIGINS,
    }


# A "todos" endpoint the React app can POST to and GET from
@app.get("/todos")
def get_todos():
    return {
        "todos": [
            {"id": 1, "title": "Learn CORS", "done": True},
            {"id": 2, "title": "Build a React app", "done": False},
        ]
    }


@app.post("/todos")
def add_todo(todo: dict):
    return {
        "message": "Todo added",
        "data": todo,
    }
