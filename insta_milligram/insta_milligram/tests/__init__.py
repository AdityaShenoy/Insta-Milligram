import django.http.response as dhres
import django.urls as du

import rest_framework.views as rv  # type: ignore

import typing as t


def generate_headers(login_response: dhres.HttpResponse):
    access_token = login_response.data["tokens"]["access"]  # type: ignore
    return {"Authorization": f"Bearer {access_token}"}


def test_url_resolution(url_name: str, view: rv.APIView, args: list[t.Any] = []):
    assert (
        du.resolve(
            du.reverse(url_name, args=args),
        ).func.cls  # type: ignore
        == view
    )
