import django.http.response as dhres

import rest_framework.response as rr  # type: ignore

import typing as t


def assertEqualResponses(
    response1: dhres.HttpResponse,
    response2: dhres.HttpResponse,
):
    assert response1.data["message"] == response2.data["message"]  # type: ignore
    assert response1.status_code == response1.status_code


def create_response(
    message: str,
    status_code: int,
    data: dict[str, t.Any] = dict(),
):
    return rr.Response({"message": message, **data}, status_code)
