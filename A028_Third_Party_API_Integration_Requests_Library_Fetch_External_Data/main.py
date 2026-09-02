# =========================================================
# A028 — Third-Party API Integration (requests library)
# =========================================================
# Proxy / wrapper routes that call an EXTERNAL JSON API:
#   - GET /posts            →  fetches all posts from jsonplaceholder
#   - GET /posts/{post_id}  →  fetches one post; 404 if the upstream returns non-200
#
# We use the `requests` library (sync, blocking) inside FastAPI sync routes.
# For high-traffic apps, see "Variations" → async with httpx.AsyncClient.
# =========================================================

# --- FastAPI: framework + HTTP error handling ---
from fastapi import FastAPI, HTTPException

# --- `requests`: the classic sync HTTP client ---
# (fastapi[standard] does NOT include it; install separately.)
import requests

# 1. Create the FastAPI app instance (Uvicorn serves THIS object)
app = FastAPI()


# =========================================================
# GET /posts — forward a list of posts from a 3rd-party API
# =========================================================
# `jsonplaceholder.typicode.com` is a free fake-REST API for testing.
# Each call returns a JSON array of 100 post objects.
@app.get("/posts")
def get_posts():
    # Hit the upstream API directly
    upstream_url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(upstream_url)

    # If the upstream is down or returns an error, bubble it up
    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Upstream API returned HTTP {response.status_code}"
        )

    # `response.json()` parses the body into a Python list/dict
    return response.json()


# =========================================================
# GET /posts/{post_id} — forward a single post
# =========================================================
# `post_id` is validated by FastAPI (must be a positive-ish int).
# If the upstream 404s, we map it to our own 404 so the client
# gets a consistent error shape.
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    upstream_url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    response = requests.get(upstream_url)

    # Map upstream errors to our own
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Post not found")
    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Upstream API returned HTTP {response.status_code}"
        )

    return response.json()


# =========================================================
# GET / — health check
# =========================================================
@app.get("/")
def home():
    return {
        "message": "A028 proxy running. Use /posts or /posts/{id}."
    }
