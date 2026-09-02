import sys
sys.path.insert(0, '.')
from main import app, initialize_user_db, fake_user_db, verify_password, create_token

# Initialize the user DB first
initialize_user_db()
print("fake_user_db after init:", fake_user_db)

# Test verify_password 
hashed = fake_user_db["admin"]["hashed_password"]
print("hashed_password exists:", hashed is not None)
if hashed:
    result = verify_password("1234", hashed)
    print("verify_password result:", result)

# Test create_token
token = create_token({"sub": "admin"})
print("Token created:", token[:50], "...")