import django.http.request as dhreq

from . import generate_tokens as g
from . import refresh_tokens as r
import insta_milligram.constants.responses as icr


def post(request: dhreq.HttpRequest):
    action = request.GET.get("action")
    if action not in ["generate", "refresh"]:
        return icr.INCORRECT_TOKEN_PARAMETER
    if action == "generate":
        return g.generate_tokens(request)
    return r.refresh_tokens(request)
