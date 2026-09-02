# =========================================================
# A026 — Environment Variables (.env + python-dotenv)
# =========================================================
# Centralised config module:
#   - Loads .env once at import time
#   - Parses JSON lists (ORIGINS) into Python lists
#   - Exposes values via a Settings instance
# =========================================================

# --- stdlib: read env vars ---
import os

# --- python-dotenv: load .env into os.environ ---
# `load_dotenv()` reads a `.env` file in the current working directory
# and merges its values into `os.environ`. Existing env vars WIN unless
# you pass `override=True`.
from dotenv import load_dotenv

# Load the .env file at import time so every consumer sees the values.
load_dotenv()


def _parse_list(raw: str | None) -> list[str]:
    """
    Accept two formats for the ORIGINS env var:
      1. JSON list:        ORIGINS=["http://a", "http://b"]
      2. Comma-separated:  ORIGINS=http://a,http://b

    Returns a Python list of strings either way.
    """
    if not raw:
        return []
    raw = raw.strip()
    if raw.startswith("["):
        # JSON form — safest when origins contain commas/ports/colons
        import json
        return json.loads(raw)
    # Comma-separated form — short and readable for the common case
    return [item.strip() for item in raw.split(",") if item.strip()]


class Settings:
    """
    Plain Python class holding config values.
    (For larger apps, swap this for `pydantic-settings`'s `BaseSettings`,
    which gives you type validation + a .env file path resolver out of
    the box. See "Variations" in the README.)
    """

    def __init__(self) -> None:
        # CORS allow-list — parsed from JSON or comma-separated
        self.origins: list[str] = _parse_list(os.getenv("ORIGINS"))

        # JWT secret (used by A022 / A023 in real apps)
        self.SECRET_KEY: str | None = os.getenv("SECRET_KEY")

        # Database connection string
        self.DB_URL: str | None = os.getenv("DB_URL")

        # App metadata
        self.APP_NAME: str = os.getenv("APP_NAME", "FastAPI App")
        self.DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")


# Singleton — import this everywhere you need config
settings = Settings()
