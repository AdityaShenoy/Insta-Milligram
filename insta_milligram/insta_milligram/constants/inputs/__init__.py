LOGIN_REQUEST = {"username": "test", "password": "testpass"}

SIGNUP_REQUEST = {
    **LOGIN_REQUEST,
    "email": "test@test.com",
    "first_name": "test",
    "last_name": "test",
}

UPDATE_REQUEST = {k: f"new_{v}" for k, v in SIGNUP_REQUEST.items()}
