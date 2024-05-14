import django.contrib.auth.models as dcam
import django.http.request as dhreq

import rest_framework_simplejwt.views as jv

from ... import forms as f
import insta_milligram.constants as ic
import insta_milligram.forms as if_
import insta_milligram.responses as ir
import insta_milligram.responses.decorators as ird


@ird.check_form(f.GenerateTokenForm)
def generate_tokens(request: dhreq.HttpRequest):
    form_data = if_.get_data(f.GenerateTokenForm(request.POST))
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
