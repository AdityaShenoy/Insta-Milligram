import django.contrib.auth.models as dcam
import django.http.request as dhreq

import insta_milligram.constants.responses as icr
import insta_milligram.responses as ir
import insta_milligram.responses.decorators as ird
import users.serializers as us


@ird.check_authenticated()
@ird.check_missing_id()
@ird.check_user_exists()
def get(request: dhreq.HttpRequest, id: int = -1):
    user = dcam.User.objects.get(pk=id)
    serialized_user = us.UserSerializer(user)
    return ir.create_response(
        icr.SUCCESS,
        serialized_user.data,  # type: ignore
    )
