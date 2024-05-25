import django.http.request as dhreq

import insta_milligram.constants.responses as icr
import insta_milligram.responses.decorators as ird
import users.models.profiles as ump


@ird.check_authenticated()
@ird.check_missing_id()
@ird.check_user_exists()
@ird.check_authorized()
def patch(request: dhreq.HttpRequest, id: int = -1):
    patch_inputs = {*request.POST.keys(), *request.FILES.keys()}
    if not {"profile_picture", "bio"} & patch_inputs:
        return icr.INVALID_USER_PATCH_DATA

    profile = ump.Profile.objects.get(pk=id)

    if "profile_picture" in patch_inputs:

        profile_picture = request.FILES["profile_picture"]  # type: ignore
        profile.picture = profile_picture  # type: ignore
        profile.save()  # type: ignore

    return icr.SUCCESS
