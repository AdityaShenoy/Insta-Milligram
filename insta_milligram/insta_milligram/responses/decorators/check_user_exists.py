import django.contrib.auth.models as dcam

import rest_framework.response as rr  # type: ignore

import typing as t

import insta_milligram.constants as ic

func_type = t.Callable[..., rr.Response]


def check_user_exists():
    def decorator(func: func_type):
        def wrapper(*args: t.Any, **kwargs: t.Any):
            user_id = kwargs.get("id")
            try:
                dcam.User.objects.get(pk=user_id)
            except dcam.User.DoesNotExist:
                return ic.responses.USER_NOT_FOUND

            return func(*args, **kwargs)

        return wrapper

    return decorator
