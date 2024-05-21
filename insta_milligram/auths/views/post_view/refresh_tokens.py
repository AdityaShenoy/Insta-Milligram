import django.http.request as dhreq

import rest_framework_simplejwt.views as jv

import auths.forms as af
import insta_milligram.constants as ic
import insta_milligram.responses as ir
import insta_milligram.responses.decorators as ird


@ird.check_form(af.RefreshTokenForm)
def refresh_tokens(request: dhreq.HttpRequest):
    response = jv.token_refresh(request._request)  # type: ignore
    if ("code" in response.data) and (  # type: ignore
        response.data["code"].code == "token_not_valid"  # type: ignore
    ):
        return ic.responses.INVALID_TOKEN
    return ir.create_response(
        ic.responses.SUCCESS,
        response.data,  # type: ignore
    )
