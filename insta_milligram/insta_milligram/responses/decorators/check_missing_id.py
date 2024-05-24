import rest_framework.response as rr  # type: ignore

import typing as t

import insta_milligram.constants.responses as icr

func_type = t.Callable[..., rr.Response]


def check_missing_id():
    def decorator(func: func_type):
        def wrapper(*args: t.Any, **kwargs: t.Any):
            user_id = kwargs.get("id", -1)
            if user_id == -1:
                return icr.USER_ID_MISSING

            return func(*args, **kwargs)

        return wrapper

    return decorator
