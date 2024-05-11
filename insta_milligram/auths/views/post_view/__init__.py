import django.http.request as dr

import rest_framework.response as rr  # type: ignore
import rest_framework.status as rs  # type: ignore

from . import generate_tokens as g
from . import refresh_tokens as r


def post(request: dr.HttpRequest):
    action = request.GET.get("action")
    if action not in ["generate", "refresh"]:
        # todo: move this to constants
        return rr.Response(
            {
                "message": "Incorrect Parameter - "
                + "Expected ?action=generate or ?action=refresh"
            },
            rs.HTTP_400_BAD_REQUEST,
        )
    if action == "generate":
        return g.generate_tokens(request)
    return r.refresh_tokens(request)
