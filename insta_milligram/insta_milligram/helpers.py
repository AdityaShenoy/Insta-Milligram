import django.http.response as dres

import rest_framework.response as rr  # type: ignore

import typing as t


def assertEqualResponse(
    response1: dres.HttpResponse,
    message: str,
    status_code: int,
):
    assert response1.data["message"] == message  # type: ignore
    assert response1.status_code == status_code


def create_response(
    message: str,
    status_code: int,
    data: dict[str, t.Any] = dict(),
):
    return rr.Response({"message": message, **data}, status_code)
