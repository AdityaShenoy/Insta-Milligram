import rest_framework.response as rr  # type: ignore

import rest_framework_simplejwt.exceptions as je
import rest_framework_simplejwt.tokens as jt

import typing as t

import auths.get_auth_user as ag
import auths.models as am
import insta_milligram.constants as ic

func_type = t.Callable[..., rr.Response]


def check_authenticated():
    def decorator(func: func_type):
        def wrapper(*args: t.Any, **kwargs: t.Any):
            request = args[0]._request
            try:
                user = ag.get_auth_user(request)
                token = request.headers.get("Authorization").split()[1]
                iat = int(jt.AccessToken(token).payload["iat"])  # type: ignore
                existing_logout_entry = am.BlacklistedToken.objects.filter(
                    user=user,
                )
                if existing_logout_entry:
                    logout_iat = existing_logout_entry[0].iat
                    if iat <= logout_iat:
                        return ic.responses.LOGIN_BLACKLISTED

                return func(*args, **kwargs)
            except TypeError:
                return ic.responses.TOKEN_MISSING
            except je.InvalidToken:
                return ic.responses.INVALID_TOKEN
            except je.AuthenticationFailed:
                return ic.responses.USER_NOT_FOUND

        return wrapper

    return decorator
