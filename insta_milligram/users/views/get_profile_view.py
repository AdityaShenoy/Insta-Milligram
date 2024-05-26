import django.http.request as dhreq

import insta_milligram.constants.responses as icr
import insta_milligram.responses as ir
import insta_milligram.responses.decorators as ird
import users.models.profiles as ump
import users.serializers as us


@ird.check_authenticated()
@ird.check_user_exists()
def get(request: dhreq.HttpRequest, id: int = -1):
    profile = ump.Profile.objects.get(pk=id)
    serialized_profile = us.ProfileSerializer(profile)
    return ir.create_response(
        icr.SUCCESS,
        {"profile": serialized_profile.data},  # type: ignore
    )
