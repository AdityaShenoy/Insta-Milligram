import django.http.response as dhres
import django.urls as du

import rest_framework.response as rr  # type: ignore
import rest_framework.views as rv  # type: ignore

import typing as t


def assertEqualResponse(
    response: dhres.HttpResponse,
    message: str,
    status_code: int,
):
    assert response.data["message"] == message  # type: ignore
    assert response.status_code == status_code


def assertEqualResponses(
    response1: dhres.HttpResponse,
    response2: dhres.HttpResponse,
):
    assert response1.data == response2.data  # type: ignore
    assert response1.status_code == response1.status_code


def create_response(
    message: str,
    status_code: int,
    data: dict[str, t.Any] = dict(),
):
    return rr.Response({"message": message, **data}, status_code)


def generate_headers(login_response: dhres.HttpResponse):
    access_token = login_response.data["tokens"]["access"]  # type: ignore
    return {"Authorization": f"Bearer {access_token}"}


def test_url_resolution(url_name: str, view: rv.APIView, args: list[t.Any] = []):
    assert du.resolve(du.reverse(url_name, args=args)).func.cls == view  # type: ignore
