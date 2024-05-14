import django.http.request as dhreq
import django.contrib.auth.models as dcam

import rest_framework.status as rs  # type: ignore

import insta_milligram.constants as c
import insta_milligram.responses as r
import auths.views as v


def get(request: dhreq.HttpRequest, id: int, id1: int = -1):
    response = v.get(request, id)
    user = response.data.get("user")  # type: ignore
    if not user:
        return response

    try:
        user = dcam.User.objects.get(pk=id)
    except dcam.User.DoesNotExist:
        return c.responses.USER_NOT_FOUND

    # todo: paginate the users list instead of sending user ids
    if id1 == -1:
        followings = user.followings.all().values_list(  # type: ignore
            "following", flat=True
        )
        return r.create_response(
            c.responses.SUCCESS,
            {"followings": followings},
        )

    try:
        followed_user = dcam.User.objects.get(pk=id1)
    except dcam.User.DoesNotExist:
        return c.responses.USER_NOT_FOUND

    is_following = user.followings.filter(  # type: ignore
        following=followed_user,
    ).exists()
    return r.create_response(
        c.responses.SUCCESS,
        {"is_following": is_following},
    )
