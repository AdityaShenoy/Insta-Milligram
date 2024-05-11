LOGIN_REQUEST = {"username": "test", "password": "testpass"}
LOGIN_REQUEST_1 = {"username": "test1", "password": "test1pass"}

SIGNUP_REQUEST = {
    **LOGIN_REQUEST,
    "email": "test@test.com",
    "first_name": "test",
    "last_name": "test",
}

SIGNUP_REQUEST_1 = {
    **LOGIN_REQUEST_1,
    "email": "test1@test1.com",
    "first_name": "test1",
    "last_name": "test1",
}

UPDATE_REQUEST = {k: f"new_{v}" for k, v in SIGNUP_REQUEST.items()}

EXPIRED_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE1MTQ3MzU5LCJpYXQiOjE3MTUxNDcwNTksImp0aSI6IjYxNzlkMGQ5NTk1MTQ3NTdiMGU5YTA4ZjQ2YmRiMDY5IiwidXNlcl9pZCI6MX0.0q-rm-CvDISZyR4Pksfv5Ik00ltAyV5IK2SAsHb1KaI"
