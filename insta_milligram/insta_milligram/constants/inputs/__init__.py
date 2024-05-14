NUM_USERS = 15

LOGIN_REQUESTS = [
    {
        "username": f"test_{i}",
        "password": f"test_{i}_pass",
    }
    for i in range(NUM_USERS)
]

SIGNUP_REQUESTS = [
    {
        **LOGIN_REQUESTS[i],
        "email": f"test_{i}@test.com",
        "first_name": f"test_{i}",
        "last_name": f"test_{i}",
    }
    for i in range(NUM_USERS)
]

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

UPDATE_REQUESTS = [
    {k: f"new_{v}" for k, v in SIGNUP_REQUESTS[i].items()}
    for i in range(len(SIGNUP_REQUESTS))
]

EXPIRED_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE1MTQ3MzU5LCJpYXQiOjE3MTUxNDcwNTksImp0aSI6IjYxNzlkMGQ5NTk1MTQ3NTdiMGU5YTA4ZjQ2YmRiMDY5IiwidXNlcl9pZCI6MX0.0q-rm-CvDISZyR4Pksfv5Ik00ltAyV5IK2SAsHb1KaI"
EXPIRED_REFRESH_TOKEN = {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTc5MzU5NCwiaWF0IjoxNzE1NzA3MTk0LCJqdGkiOiIyYTFlNTY3MDQ2NGM0NDM0OWU2YjQwZjk1M2VkOGNmNSIsInVzZXJfaWQiOjF9.i5N6J6sbj77KdRXyxsALFHmk6gjmt3tFhBhm8ibYsR4"
}

FOLLOW_REQUEST_2 = {"user": 2}
