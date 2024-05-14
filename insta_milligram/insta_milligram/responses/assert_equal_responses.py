import django.http.response as dhres


def assert_equal_responses(
    response1: dhres.HttpResponse,
    response2: dhres.HttpResponse,
):
    assert response1.data["message"] == response2.data["message"]  # type: ignore
    assert response1.status_code == response1.status_code
