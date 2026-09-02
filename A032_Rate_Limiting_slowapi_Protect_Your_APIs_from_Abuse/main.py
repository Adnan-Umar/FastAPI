# =========================================================
# A032 — Rate Limiting (slowapi) — Protect Your APIs from Abuse
# =========================================================
# What this module shows:
#   - Using `slowapi` (a FastAPI/Starlette port of Flask-Limiter)
#     to cap how often a client can call an endpoint.
#   - The `/data` endpoint is rate-limited to 5 requests/minute
#     per client IP address.
#   - A custom exception handler returns 429 when the limit is hit.
#
# Route:
#   - GET /data  → returns {"message":"Success"} (up to 5 times/min per IP)
#   - On the 6th request within the window → 429 Too Many Requests
# =========================================================

# --- FastAPI: framework + Request + JSON error responses ---
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# --- slowapi: rate-limiting middleware + decorator library ---
# `slowapi` wraps Starlette's middleware system to provide
# Flask-Limiter-style `@limiter.limit("N/minute")` decorators.
from slowapi import Limiter
from slowapi.util import get_remote_address       # function that decides the "rate-limit bucket"
from slowapi.errors import RateLimitExceeded     # the exception raised when a limit is hit

# 1. Create the FastAPI app instance (Uvicorn serves THIS object)
app = FastAPI()

# =========================================================
# LIMITER SETUP
# =========================================================
# `key_func=get_remote_address` means: clients are grouped by IP.
# Each unique IP gets its own rate-limit bucket (its own counter).
# `get_remote_address` reads `request.client.host` under the hood.
limiter = Limiter(key_func=get_remote_address)

# `slowapi` reads its config from `app.state.limiter`, so we must
# attach it here. Without this line, `@limiter.limit(...)` does nothing.
app.state.limiter = limiter

# =========================================================
# ERROR HANDLER — 429 Too Many Requests
# =========================================================
# When a client exceeds their quota, slowapi raises `RateLimitExceeded`.
# FastAPI's default 500 HTML error page is useless for a JSON API, so
# we register a custom handler that returns JSON + status 429.
@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,       # HTTP 429 = Too Many Requests
        content={
            "detail": "Too many requests"
        }
    )

# =========================================================
# RATE-LIMITED ENDPOINT — GET /data
# =========================================================
# The order of decorators matters!
#   1. `@app.get("/data")` registers the route with FastAPI first.
#   2. `@limiter.limit("5/minute")` wraps the wrapped handler
#      so that slowapi can enforce the quota before FastAPI's
#      normal dispatch.
#
# `5/minute` = at most 5 requests per minute, per IP.
# slowapi also supports: "10/hour", "100/day", "2/second", "100/minute".
@app.get("/data")
@limiter.limit("5/minute")
def get_data(request: Request):
    # (A real handler might use `request` to inspect headers, etc.)
    return {
        "message": "Success"
    }
