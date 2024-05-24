import django.http.request as dhreq

import rest_framework_simplejwt.tokens as jt

import auths.get_auth_user as ag
import auths.models as am
import insta_milligram.constants.responses as icr
import insta_milligram.responses.decorators as ird


@ird.check_authenticated()
def delete(request: dhreq.HttpRequest):
    user = ag.get_auth_user(request)
    token = jt.AccessToken.for_user(user)
    iat = int(token.payload["iat"])  # type: ignore

    existing_logout_entry = am.BlacklistedToken.objects.filter(user=user)
    if existing_logout_entry:
        existing_logout_entry[0].iat = iat
        existing_logout_entry[0].save()
    else:
        am.BlacklistedToken.objects.create(user=user, iat=iat)
    return icr.SUCCESS
