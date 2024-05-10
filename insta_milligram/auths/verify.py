import django.http.request as dr
import django.contrib.auth.models as dam

import rest_framework.response as rr  # type: ignore
import rest_framework.status as rs  # type: ignore

import rest_framework_simplejwt.authentication as ja
import rest_framework_simplejwt.exceptions as je

import typing as t

import dataclasses as dc


@dc.dataclass
class ResponseAndUser:
    response: t.Optional[rr.Response]
    user: t.Optional[dam.User]


def verify(request: dr.HttpRequest, id: int) -> ResponseAndUser:
    if id == -1:
        return ResponseAndUser(
            response=rr.Response(
                {"message": "User ID Missing"},
                rs.HTTP_400_BAD_REQUEST,
            ),
            user=None,
        )
    authentication = ja.JWTAuthentication()
    try:
        result = authentication.authenticate(request._request)  # type: ignore
        if not result:
            return ResponseAndUser(
                response=rr.Response(
                    {"message": "Token Missing"},
                    rs.HTTP_401_UNAUTHORIZED,
                ),
                user=None,
            )
        return ResponseAndUser(None, user=result[0])  # type: ignore
    except je.InvalidToken:
        return ResponseAndUser(
            response=rr.Response(
                {"message": "Invalid Token"},
                rs.HTTP_401_UNAUTHORIZED,
            ),
            user=None,
        )
    except je.AuthenticationFailed:
        return ResponseAndUser(
            response=rr.Response({"message": "User Not Found"}, rs.HTTP_404_NOT_FOUND),
            user=None,
        )
