# =========================================================
# A026 — Environment Variables (.env + python-dotenv)
# =========================================================
# Demonstrates:
#   - Loading config from a .env file (via python-dotenv)
#   - Using the Settings singleton from config.py
#   - CORS allow-list sourced from the env (not hard-coded)
#   - Exposing NON-SENSITIVE config via a /config endpoint
# =========================================================

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
        "db_url_scheme": (settings.DB_URL or "").split("://", 1)[0],    # e.g. "sqlite"
    }
