import django.http.request as dhreq

import rest_framework.response as rr  # type: ignore

import rest_framework_simplejwt.tokens as jt

import typing as t

import auths.get_auth_user as ag
import auths.models as am

func_type = t.Callable[..., rr.Response]


def check_blacklisted(request: dhreq.HttpRequest):
    user = ag.get_auth_user(request)
    token = request.headers.get("Authorization", "a b").split()[1]
    iat = int(jt.AccessToken(token).payload["iat"])  # type: ignore
    existing_logout_entry = am.BlacklistedToken.objects.filter(user=user)
    return existing_logout_entry and existing_logout_entry[0].iat >= iat
