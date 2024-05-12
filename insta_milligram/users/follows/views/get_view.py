import django.http.request as dhreq
import django.contrib.auth.models as dcam

import rest_framework.status as rs  # type: ignore

import insta_milligram.constants as c
import insta_milligram.helpers as h
import auths.views as v


def get(request: dhreq.HttpRequest, id: int):
    response = v.get(request, id)
    user = response.data.get("user")  # type: ignore
    if not user:
        return response

    try:
        user = dcam.User.objects.get(pk=id)
    except dcam.User.DoesNotExist:
        return c.responses.USER_NOT_FOUND

    followings = user.followings.all().values_list(  # type: ignore
        "following", flat=True
    )
    return h.create_response(
        c.messages.SUCCESS,
        rs.HTTP_200_OK,
        {"followings": followings},
    )
