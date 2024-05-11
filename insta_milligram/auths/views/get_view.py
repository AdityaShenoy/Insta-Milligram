import django.http.request as dhreq

import rest_framework.status as rs  # type: ignore

import rest_framework_simplejwt.authentication as ja
import rest_framework_simplejwt.exceptions as je


import insta_milligram.constants as c
import insta_milligram.helpers as h


def get(request: dhreq.HttpRequest, id: int):
    if id == -1:
        return c.responses.USER_ID_MISSING
    try:
        result = ja.JWTAuthentication().authenticate(request._request)  # type: ignore
        if result:
            return h.create_response(
                c.messages.SUCCESS, rs.HTTP_200_OK, {"user": result[0]}
            )
        return c.responses.TOKEN_MISSING
    except je.InvalidToken:
        return c.responses.INVALID_TOKEN
    except je.AuthenticationFailed:
        return c.responses.USER_NOT_FOUND
