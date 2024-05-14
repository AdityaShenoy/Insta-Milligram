import django.http.response as dhres


def generate_headers(login_response: dhres.HttpResponse):
    access_token = login_response.data["tokens"]["access"]  # type: ignore
    return {"Authorization": f"Bearer {access_token}"}
