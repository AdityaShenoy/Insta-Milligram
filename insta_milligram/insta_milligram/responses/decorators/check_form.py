import django.forms as df

import rest_framework.response as rr  # type: ignore
import rest_framework.status as rs  # type: ignore

import typing as t

import insta_milligram.constants as ic
import insta_milligram.responses as ir

func_type = t.Callable[..., rr.Response]


def check_form(form_class: t.Callable[..., df.Form]):
    def decorator(func: func_type):
        def wrapper(*args: t.Any, **kwargs: dict[str, t.Any]):
            request = args[0]
            form = form_class(request.POST)
            if not form.is_valid():
                return ir.create_response(
                    ic.messages.INVALID_DATA,
                    rs.HTTP_400_BAD_REQUEST,
                    {"errors": form.errors},
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator