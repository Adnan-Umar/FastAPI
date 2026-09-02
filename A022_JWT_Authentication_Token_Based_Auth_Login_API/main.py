# =========================================================
# A022 — JWT Authentication (Token-Based Auth / Login API)
# =========================================================
# Walks the full JWT flow:
#   - POST /login              → check username/password, return a signed JWT
#   - GET  /secure             → requires a valid JWT in the Authorization header
#   - The token is signed with HS256 + a secret key
#   - It carries an `exp` claim so it expires after 30 minutes
# =========================================================

# --- FastAPI: framework + HTTP errors + Header param + DI ---
from fastapi import FastAPI, HTTPException, Depends, Header

# --- python-jose: encode and decode JWTs ---
# "jose" stands for "Javascript Object Signing and Encryption"
from jose import jwt

# --- stdlib: timestamps for token expiry ---
from datetime import datetime, timedelta, timezone

# 1. Create the FastAPI app instance (Uvicorn serves THIS object)
app = FastAPI()

# 2. The secret key used to SIGN and VERIFY tokens
#    ⚠️  In production: load from env, never commit a real secret.
SECRET_KEY = "mysecret"

# 3. The signing algorithm (HMAC-SHA256 — symmetric, fast, common)
ALGORITHM = "HS256"


# =========================================================
# CREATE TOKEN — helper
# =========================================================
# Build the payload, attach an `exp` claim, sign it, return the JWT string.
def create_token(data: dict) -> str:
    # Copy the input so we don't mutate the caller's dict
    to_encode = data.copy()

    # Set expiry: now + 30 minutes (timezone-aware UTC)
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})

    # Sign the payload with the secret + algorithm → JWT string
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


# =========================================================
# LOGIN — POST /login  (issues a JWT)
# =========================================================
# Body: ?username=...&password=...
# On success: { "access_token": "<jwt>" }
# On failure: 401 Invalid username and password
@app.post("/login")
def login(username: str, password: str):
    # Toy check — in reality you'd hash + compare against a DB
    if username != "admin" or password != "1234":
        raise HTTPException(
            status_code=401,
            detail="Invalid username and password"
        )

    # `sub` (subject) is the standard claim for "who is this token for?"
    token = create_token({"sub": username})

    return {
        "access_token": token
    }


# =========================================================
# VERIFY TOKEN — dependency used by protected routes
# =========================================================
# Reads the raw token from a custom header, decodes it,
# and either returns the payload or raises 401.
def verify_token(token: str = Header(None)):
    try:
        # Decode verifies the signature AND the `exp` claim automatically
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        # Any failure (bad signature, expired, malformed) → 401
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


# =========================================================
# PROTECTED ROUTE — GET /secure
# =========================================================
# `Depends(verify_token)` runs the verifier before this handler;
# if it raises, the handler never runs.
@app.get("/secure")
def secure_data(user=Depends(verify_token)):
    return {
        "message": "Secured data accessed",
        "user": user
    }
