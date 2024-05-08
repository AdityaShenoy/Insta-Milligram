import django.http.request as dr

import rest_framework.response as rr  # type: ignore
import rest_framework.status as rs  # type: ignore

import rest_framework_simplejwt.authentication as ja
import rest_framework_simplejwt.exceptions as je


def delete(request: dr.HttpRequest, id: int = -1):
    if id == -1:
        return rr.Response(
            {"message": "User ID Missing"},
            rs.HTTP_400_BAD_REQUEST,
        )
    authentication = ja.JWTAuthentication()
    try:
        result = authentication.authenticate(request._request)  # type: ignore
        if not result:
            return rr.Response(
                {"message": "Token Missing"},
                rs.HTTP_401_UNAUTHORIZED,
            )
        user = result[0]  # type: ignore
        if not user.id == id:  # type: ignore
            return rr.Response(
                {"message": "Operation Not Allowed"},
                rs.HTTP_403_FORBIDDEN,
            )
        user.delete()  # type: ignore
        return rr.Response({"message": "Success"}, rs.HTTP_200_OK)
    except je.InvalidToken:
        return rr.Response(
            {"message": "Invalid Token"},
            rs.HTTP_401_UNAUTHORIZED,
        )
    except je.AuthenticationFailed:
        return rr.Response({"message": "User Not Found"}, rs.HTTP_404_NOT_FOUND)
