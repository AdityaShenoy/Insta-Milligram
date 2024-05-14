import django.http.request as dhreq

import rest_framework_simplejwt.authentication as ja
import rest_framework_simplejwt.exceptions as je

import insta_milligram.constants as ic
import insta_milligram.responses as ir

# todo: delete this file after removing dependencies


def get(request: dhreq.HttpRequest, id: int):
    if id == -1:
        return ic.responses.USER_ID_MISSING
    try:
        result = ja.JWTAuthentication().authenticate(  # type: ignore
            request._request,  # type: ignore
        )
        if result:
            return ir.create_response(ic.responses.SUCCESS, {"user": result[0]})
        return ic.responses.TOKEN_MISSING
    except je.InvalidToken:
        return ic.responses.INVALID_TOKEN
    except je.AuthenticationFailed:
        return ic.responses.USER_NOT_FOUND
