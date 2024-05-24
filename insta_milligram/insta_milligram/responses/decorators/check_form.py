import django.forms as df

import rest_framework.response as rr  # type: ignore

import typing as t

import insta_milligram.constants.responses as icr
import insta_milligram.responses as ir

func_type = t.Callable[..., rr.Response]


def check_form(form_class: t.Callable[..., df.Form]):
    def decorator(func: func_type):
        def wrapper(*args: t.Any, **kwargs: dict[str, t.Any]):
            request = args[0]
            form = form_class(request.data)
            if not form.is_valid():
                return ir.create_response(icr.INVALID_DATA, {"errors": form.errors})

            return func(*args, **kwargs)

        return wrapper

    return decorator
