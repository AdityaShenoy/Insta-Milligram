import django.http.request as dhreq
import django.contrib.auth.models as dcam

import rest_framework.status as rs  # type: ignore

import insta_milligram.constants as c
import insta_milligram.responses as r
import auths.views as v


def get_followers(request: dhreq.HttpRequest, id: int):
    response = v.get(request, id)
    user = response.data.get("user")  # type: ignore
    if not user:
        return response

    try:
        user = dcam.User.objects.get(pk=id)
    except dcam.User.DoesNotExist:
        return c.responses.USER_NOT_FOUND

    # todo: paginate the users list instead of sending user ids
    followers = user.followers.all().values_list(  # type: ignore
        "follower",
        flat=True,
    )
    return r.create_response(c.responses.SUCCESS, {"followers": followers})
