import django.http.request as dhreq
import django.contrib.auth.models as dcam
import django.db.transaction as ddt

import rest_framework.status as rs  # type: ignore

from .. import forms as f
import insta_milligram.constants as c
import insta_milligram.responses as r
import auths.views as v
import users.models.users_follows as umuf


def post(request: dhreq.HttpRequest, id: int):
    response = v.get(request, id)
    user = response.data.get("user")  # type: ignore
    if not user:
        return response

    form = f.UserFollowForm(request.POST)
    if not form.is_valid():
        return r.create_response(
            c.messages.INVALID_DATA,
            rs.HTTP_400_BAD_REQUEST,
            {"errors": form.errors},
        )

    form_data = form.cleaned_data
    followed_users = dcam.User.objects.filter(pk=form_data["user"])
    if not followed_users:
        return c.responses.USER_NOT_FOUND
    followed_user = followed_users[0]
    if followed_user == user:
        return c.responses.OPERATION_NOT_ALLOWED

    is_already_following = umuf.UserFollow.objects.filter(
        follower=user, following=followed_user
    ).exists()
    if is_already_following:
        return c.responses.OPERATION_NOT_ALLOWED

    with ddt.atomic():
        umuf.UserFollow.objects.create(
            follower=user,
            following=followed_user,
        )
        followed_user.profile.followers_count += 1  # type: ignore
        user.profile.followings_count += 1  # type: ignore
        followed_user.profile.save()  # type: ignore
        user.profile.save()  # type: ignore
    return c.responses.SUCCESS
