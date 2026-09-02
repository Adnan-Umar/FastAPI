# =========================================================
# A027 — API Testing with Pytest (Test Endpoints)
# =========================================================
# A tiny app to test:
#   - GET /        → health check
#   - GET /add     → query-param arithmetic
# =========================================================

from fastapi import FastAPI

# 1. Create the FastAPI app instance
app = FastAPI()


@app.get("/")
def home():
    """Health check / hello endpoint."""
    return {
        "message": "Hello Adnan"
    }


@app.get("/add")
def add(a: int, b: int):
    """
    Add two integers.
    Both `a` and `b` come from query params and are coerced to int
    by FastAPI's type-driven validation. Missing or non-numeric
    values return 422 before this function runs.
    """
    return {
        "result": a + b
    }
