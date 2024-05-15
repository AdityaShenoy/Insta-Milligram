import django.contrib.auth.models as dcam
import django.http.request as dhreq

import insta_milligram.constants as ic
import insta_milligram.responses as ir
import auths.views as av


def get_followers(request: dhreq.HttpRequest, id: int):
    response = av.get(request, id)
    user = response.data.get("user")  # type: ignore
    if not user:
        return response

    try:
        user = dcam.User.objects.get(pk=id)
    except dcam.User.DoesNotExist:
        return ic.responses.USER_NOT_FOUND

    # todo: paginate the users list instead of sending user ids
    followers = user.followers.all().values_list(  # type: ignore
        "follower",
        flat=True,
    )
    return ir.create_response(ic.responses.SUCCESS, {"followers": followers})
