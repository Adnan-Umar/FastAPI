# =========================================================
# A023 — OAuth2 + JWT + Password Hashing
# =========================================================
# Production-shaped auth flow:
#   - POST /login              → OAuth2PasswordRequestForm (form-encoded),
#                                verifies the password against a hashed one,
#                                returns a signed JWT (HS256, exp claim)
#   - GET  /secure             → requires a valid JWT in the Authorization
#                                header (Authorization: Bearer <token>)
#   - Passwords are NEVER stored in plain text — passlib hashes them
# =========================================================

# --- FastAPI: framework + HTTP errors + DI ---
from fastapi import FastAPI, HTTPException, Depends

# --- FastAPI security: OAuth2 form helper + Bearer token scheme ---
# OAuth2PasswordRequestForm reads `username` & `password` from an
#   application/x-www-form-urlencoded body (NOT a JSON body).
# OAuth2PasswordBearer tells Swagger UI to add the "Authorize" button
#   and tells clients to send `Authorization: Bearer <token>`.
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# --- python-jose: encode and decode JWTs ---
# "jose" = Javascript Object Signing and Encryption
from jose import jwt, JWTError

# --- stdlib: timestamps for token expiry ---
from datetime import datetime, timedelta, timezone

# --- passlib: password hashing (sha256_crypt — works on Python 3.13/3.14) ---
from passlib.context import CryptContext

# 1. Create the FastAPI app instance (Uvicorn serves THIS object)
app = FastAPI()


# =========================================================
# JWT CONFIG
# =========================================================
# ⚠️  In production: load from env, never commit a real secret.
SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# =========================================================
# PASSWORD HASHING SETUP
# =========================================================
# `sha256_crypt` is a pure-Python passlib scheme; it avoids the native
# `bcrypt` module's compatibility issues with newer Python versions.
pwd_context = CryptContext(schemes=["sha256_crypt"])


# =========================================================
# DUMMY USER "DATABASE"
# =========================================================
# In a real app this is a SQL table. Here it's a one-row dict.
# We initialize the hash lazily on first login attempt (see below).
fake_user_db: dict[str, dict] = {
    "admin": {
        "username": "admin",
        "hashed_password": None,    # filled in on first use
    }
}


def _initialize_user_db() -> None:
    """Hash the seed password once, the first time a login is attempted."""
    if fake_user_db["admin"]["hashed_password"] is None:
        fake_user_db["admin"]["hashed_password"] = pwd_context.hash("1234")


# =========================================================
# OAUTH2 SCHEME
# =========================================================
# `tokenUrl="login"` points Swagger UI's "Authorize" button at /login.
# This also makes the OpenAPI schema advertise Bearer auth to clients.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# =========================================================
# PASSWORD HELPERS
# =========================================================
def hash_password(password: str) -> str:
    """Hash a plain-text password (use when *registering* a user)."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Constant-time compare of plain vs hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


# =========================================================
# CREATE TOKEN — helper
# =========================================================
def create_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    """Build the payload, attach an `exp` claim, sign it, return the JWT."""
    to_encode = data.copy()

    # Set expiry: now + N minutes (timezone-aware UTC — required by jose)
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})

    # Sign the payload with the secret + algorithm → JWT string
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# =========================================================
# LOGIN — POST /login  (issues a JWT)
# =========================================================
# `OAuth2PasswordRequestForm` reads `username` & `password` from the
# `application/x-www-form-urlencoded` body, NOT from query params and
# NOT from a JSON body. That is the OAuth2 spec.
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    _initialize_user_db()    # lazy hash on first login attempt

    user = fake_user_db.get(form_data.username)
    # Always do the verify (even if user is missing) to avoid leaking
    # whether a username exists. Here we just do the simple check.
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=400,
            detail="Invalid username or password"
        )

    access_token = create_token({"sub": user["username"]})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================================================
# VERIFY TOKEN — dependency used by protected routes
# =========================================================
def verify_token(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Reads the JWT from the Authorization: Bearer header (via oauth2_scheme),
    verifies the signature and `exp`, and returns a small dict identifying
    the user. Raises 401 on any failure.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        # Catches: bad signature, expired token, malformed token, wrong alg
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token (no subject)")

    return {"username": username}


# =========================================================
# PROTECTED ROUTE — GET /secure
# =========================================================
# `Depends(verify_token)` runs the verifier before this handler;
# if it raises, the handler never runs.
@app.get("/secure")
def secure_data(user: dict = Depends(verify_token)):
    return {
        "message": "Hello you have access to secure data!",
        "data": user
    }
