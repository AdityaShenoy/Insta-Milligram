import rest_framework.response as rr  # type: ignore

import typing as t

import auths.get_auth_user as ag
import insta_milligram.constants.responses as icr

func_type = t.Callable[..., rr.Response]


def check_authorized():
    def decorator(func: func_type):
        def wrapper(*args: t.Any, **kwargs: t.Any):
            request = args[0]._request
            user_id = kwargs["id"]
            user = ag.get_auth_user(request)
            if user.id != user_id:  # type: ignore
                return icr.OPERATION_NOT_ALLOWED
            return func(*args, **kwargs)

        return wrapper

    return decorator
