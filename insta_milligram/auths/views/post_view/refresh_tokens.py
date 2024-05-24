import django.contrib.auth.models as dcam
import django.http.request as dhreq

import rest_framework_simplejwt.exceptions as je
import rest_framework_simplejwt.tokens as jt

import auths.forms as af
import auths.models as am
import insta_milligram.constants.responses as icr
import insta_milligram.forms as if_
import insta_milligram.responses as ir
import insta_milligram.responses.decorators as ird


@ird.check_form(af.RefreshTokenForm)
def refresh_tokens(request: dhreq.HttpRequest):
    form_data = if_.get_data(af.RefreshTokenForm(request.POST))
    refresh_token_str = form_data["refresh"]
    try:
        refresh_token = jt.RefreshToken(refresh_token_str)
    except je.TokenError:
        return icr.INVALID_TOKEN

    iat = int(refresh_token.payload["iat"])
    user_id = int(refresh_token.payload["user_id"])
    try:
        user = dcam.User.objects.get(id=user_id)
    except dcam.User.DoesNotExist:
        return icr.USER_NOT_FOUND

    existing_logout_entry = am.BlacklistedToken.objects.filter(user=user)
    if existing_logout_entry and (existing_logout_entry[0].iat >= iat):
        return icr.LOGIN_BLACKLISTED

    access_token = refresh_token.access_token

    return ir.create_response(
        icr.SUCCESS,
        {"access": str(access_token)},
    )
