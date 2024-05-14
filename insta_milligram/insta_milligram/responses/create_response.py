import rest_framework.response as rr  # type: ignore

import typing as t


def create_response(
    response: rr.Response,
    data: dict[str, t.Any] = dict(),
):
    return rr.Response(
        {"message": response.data["message"], **data},  # type: ignore
        response.status_code,
    )
