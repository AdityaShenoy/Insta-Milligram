import rest_framework.response as rr  # type: ignore

import rest_framework_simplejwt.exceptions as je

import typing as t

import auths.get_auth_user as ag
import insta_milligram.constants as ic

func_type = t.Callable[..., rr.Response]


def check_authenticated():
    def decorator(func: func_type):
        def wrapper(*args: t.Any, **kwargs: t.Any):
            request = args[0]._request
            try:
                ag.get_auth_user(request)
                return func(*args, **kwargs)
            except TypeError:
                return ic.responses.TOKEN_MISSING
            except je.InvalidToken:
                return ic.responses.INVALID_TOKEN
            except je.AuthenticationFailed:
                return ic.responses.USER_NOT_FOUND

        return wrapper

    return decorator
