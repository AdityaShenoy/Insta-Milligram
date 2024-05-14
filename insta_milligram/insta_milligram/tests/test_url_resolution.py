import django.urls as du

import rest_framework.views as rv  # type: ignore

import typing as t


def test_url_resolution(url_name: str, view: rv.APIView, args: list[t.Any] = []):
    assert (
        du.resolve(
            du.reverse(url_name, args=args),
        ).func.cls  # type: ignore
        == view
    )
