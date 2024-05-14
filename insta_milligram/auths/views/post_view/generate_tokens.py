import django.http.request as dr
import django.contrib.auth.models as dcam

import rest_framework_simplejwt.views as jv

from ... import forms as f
import insta_milligram.constants as ic
import insta_milligram.responses as ir


def generate_tokens(request: dr.HttpRequest):
    form = f.GenerateTokenForm(request.POST)
    if not form.is_valid():
        return ir.create_response(
            ic.responses.INVALID_DATA,
            {"errors": form.errors},
        )
    form_data = form.cleaned_data
    try:
        user = dcam.User.objects.get(username=form_data["username"])
        if not user.check_password(form_data["password"]):
            return ic.responses.INCORRECT_PASSWORD
        tokens = jv.token_obtain_pair(request._request)  # type: ignore
        return ir.create_response(
            ic.responses.SUCCESS,
            {"tokens": tokens.data},  # type: ignore
        )

    except dcam.User.DoesNotExist:
        return ic.responses.INCORRECT_USER
