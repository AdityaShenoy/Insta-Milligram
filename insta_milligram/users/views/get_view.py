import django.contrib.auth.models as dcam
import django.http.request as dhreq

from .. import serializers as s
import insta_milligram.constants as ic
import insta_milligram.responses as ir
import insta_milligram.responses.decorators as ird


@ird.check_authenticated()
@ird.check_missing_id()
@ird.check_user_exists()
def get(request: dhreq.HttpRequest, id: int = -1):
    user = dcam.User.objects.get(pk=id)
    serialized_user = s.UserSerializer(user)
    return ir.create_response(
        ic.responses.SUCCESS,
        serialized_user.data,  # type: ignore
    )
