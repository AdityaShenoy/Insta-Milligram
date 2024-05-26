import django.conf as dc
import django.core.files.uploadedfile as dcfu


def signup_request(i: int):
    return {
        "username": f"test_{i}",
        "password": f"test_{i}_pass",
        "email": f"test_{i}@test.com",
        "first_name": f"test_{i}",
        "last_name": f"test_{i}",
    }


def update_request(i: int):
    return {k: f"new_{v}" for k, v in signup_request(i).items()}


def follow_request(i: int):
    return {"user": i}


DUMMY_EMAIL = {"email": "dummy@dummy.com"}
DUMMY_USERNAME = {"username": "dummy"}
SMALL_PASSWORD = {"password": "dummy"}
SPECIAL_USERNAME = {"username": "@"}


LOGIN_REQUEST_FIELDS = {"username", "password"}

EXPIRED_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE1MTQ3MzU5LCJpYXQiOjE3MTUxNDcwNTksImp0aSI6IjYxNzlkMGQ5NTk1MTQ3NTdiMGU5YTA4ZjQ2YmRiMDY5IiwidXNlcl9pZCI6MX0.0q-rm-CvDISZyR4Pksfv5Ik00ltAyV5IK2SAsHb1KaI"
EXPIRED_REFRESH_TOKEN = {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTc5MzU5NCwiaWF0IjoxNzE1NzA3MTk0LCJqdGkiOiIyYTFlNTY3MDQ2NGM0NDM0OWU2YjQwZjk1M2VkOGNmNSIsInVzZXJfaWQiOjF9.i5N6J6sbj77KdRXyxsALFHmk6gjmt3tFhBhm8ibYsR4"
}

with open("insta_milligram/tests/images/test.jpg", "rb") as f:
    PROFILE_PICTURE = dcfu.SimpleUploadedFile(
        name="test.jpg", content=f.read(), content_type="image/jpeg"
    )
UPLOADED_PROFILE_PICTURE = f"{dc.settings.MEDIA_ROOT}\\profile_pictures\\test.jpg"

TEST_BIO = "test"
