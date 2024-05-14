import django.test as dt

import insta_milligram.constants as ic


def signup_and_login(client: dt.Client, signup_request: dict[str, str]):
    client.post(ic.urls.USERS, signup_request)
    login_response = client.post(
        ic.urls.AUTHS,
        signup_request,
        QUERY_STRING="action=generate",
    )
    access_token = login_response.data["tokens"]["access"]  # type: ignore
    return {"Authorization": f"Bearer {access_token}"}
