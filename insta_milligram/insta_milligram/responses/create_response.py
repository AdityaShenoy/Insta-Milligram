import rest_framework.response as rr  # type: ignore

import typing as t


def create_response(
    message: str,
    status_code: int,
    data: dict[str, t.Any] = dict(),
):
    return rr.Response({"message": message, **data}, status_code)
