import django.contrib.auth.models as dcam
import django.http.request as dhreq

import insta_milligram.constants as ic
import insta_milligram.responses as ir
import insta_milligram.responses.decorators as ird


@ird.check_authenticated()
@ird.check_user_exists()
def get(request: dhreq.HttpRequest, id: int, id1: int = -1):
    follower_id = id
    following_id = id1

    follower = dcam.User.objects.get(id=follower_id)

    if following_id == -1:
        followings = follower.followings.all().values_list(  # type: ignore
            "following", flat=True
        )
        return ir.create_response(
            ic.responses.SUCCESS,
            {"followings": followings},
        )

    try:
        following = dcam.User.objects.get(pk=following_id)
    except dcam.User.DoesNotExist:
        return ic.responses.USER_NOT_FOUND

    is_following = follower.followings.filter(  # type: ignore
        following=following,
    ).exists()
    return ir.create_response(
        ic.responses.SUCCESS,
        {"is_following": is_following},
    )
