import django.contrib.auth.models as dcam
import django.http.request as dhreq

import auths.views as av
import insta_milligram.constants as ic
import insta_milligram.responses as ir


def get(request: dhreq.HttpRequest, id: int, id1: int = -1):
    response = av.get(request, id)
    user = response.data.get("user")  # type: ignore
    if not user:
        return response

    try:
        user = dcam.User.objects.get(pk=id)
    except dcam.User.DoesNotExist:
        return ic.responses.USER_NOT_FOUND

    # todo: paginate the users list instead of sending user ids
    if id1 == -1:
        followings = user.followings.all().values_list(  # type: ignore
            "following", flat=True
        )
        return ir.create_response(
            ic.responses.SUCCESS,
            {"followings": followings},
        )

    try:
        followed_user = dcam.User.objects.get(pk=id1)
    except dcam.User.DoesNotExist:
        return ic.responses.USER_NOT_FOUND

    is_following = user.followings.filter(  # type: ignore
        following=followed_user,
    ).exists()
    return ir.create_response(
        ic.responses.SUCCESS,
        {"is_following": is_following},
    )
