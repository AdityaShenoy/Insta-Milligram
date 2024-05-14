import django.http.request as dr
import django.contrib.auth.models as dam

import rest_framework.status as rs  # type: ignore

import rest_framework_simplejwt.views as jv

from ... import forms as f
import insta_milligram.responses as r
import insta_milligram.constants as c


def generate_tokens(request: dr.HttpRequest):
    form = f.GenerateTokenForm(request.POST)
    if not form.is_valid():
        return r.create_response(
            c.messages.INVALID_DATA,
            rs.HTTP_400_BAD_REQUEST,
            {"errors": form.errors},
        )
    form_data = form.cleaned_data
    try:
        user = dam.User.objects.get(username=form_data["username"])
        if not user.check_password(form_data["password"]):
            return c.responses.INCORRECT_PASSWORD
        tokens = jv.token_obtain_pair(request._request)  # type: ignore
        return r.create_response(
            c.messages.SUCCESS,
            rs.HTTP_200_OK,
            {"tokens": tokens.data},  # type: ignore
        )

    except dam.User.DoesNotExist:
        return c.responses.INCORRECT_USER
