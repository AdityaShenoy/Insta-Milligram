import django.http.request as dr

from . import generate_tokens as g
from . import refresh_tokens as r
import insta_milligram.constants as ic


def post(request: dr.HttpRequest):
    action = request.GET.get("action")
    if action not in ["generate", "refresh"]:
        return ic.responses.INCORRECT_TOKEN_PARAMETER
    if action == "generate":
        return g.generate_tokens(request)
    return r.refresh_tokens(request)
