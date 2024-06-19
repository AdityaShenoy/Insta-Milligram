import django.http.request as dhreq

import auths.get_auth_user as ag
import insta_milligram.constants.responses as icr
import insta_milligram.responses.decorators as ird


@ird.check_authenticated()
@ird.check_missing_id()
@ird.check_user_exists()
@ird.check_authorized()
def delete(request: dhreq.HttpRequest, id: int = -1):
    user = ag.get_auth_user(request)
    user.profile.delete()  # type: ignore
    return icr.SUCCESS
