# =========================================================
# A027 — Test suite (pytest + fastapi.testclient)
# =========================================================
# Two test functions, one per endpoint:
#   - test_home:    hits GET / and checks the JSON body
#   - test_add:     hits GET /add?a=5&b=3 and checks the result
#   - test_add_validation: checks that bad input → 422
# =========================================================

# --- fastapi's built-in test client ---
# `TestClient` wraps the ASGI app and lets you call endpoints
# exactly like an HTTP client — without spinning up a real server.
from fastapi.testclient import TestClient

# --- the app under test ---
from main import app

# --- one TestClient instance, shared by all tests ---
client = TestClient(app)


# =========================================================
# Test: GET /
# =========================================================
def test_home():
    # 1. Make the request
    response = client.get("/")

    # 2. Assert the status code
    assert response.status_code == 200

    # 3. Assert the JSON body
    assert response.json() == {"message": "Hello Adnan"}


# =========================================================
# Test: GET /add?a=5&b=3
# =========================================================
def test_add():
    response = client.get("/add?a=5&b=3")

    # 200 OK
    assert response.status_code == 200

    # body is {"result": 8}
    assert response.json() == {"result": 8}


# =========================================================
# Test: GET /add with bad input → 422
# =========================================================
def test_add_validation_error():
    # Missing required query param `b` → 422 Unprocessable Entity
    response = client.get("/add?a=5")
    assert response.status_code == 422

    # Non-numeric `b` → also 422
    response = client.get("/add?a=5&b=hello")
    assert response.status_code == 422
