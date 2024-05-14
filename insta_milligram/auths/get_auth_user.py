import django.contrib.auth.models as dcam
import django.http.request as dhreq

import rest_framework_simplejwt.authentication as ja


def get_auth_user(request: dhreq.HttpRequest) -> dcam.User:
    return ja.JWTAuthentication().authenticate(request)[0]  # type: ignore
