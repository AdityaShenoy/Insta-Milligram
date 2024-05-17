import django.contrib.auth.models as dcam
import django.db.transaction as ddt
import django.http.request as dhreq

import auths.get_auth_user as ag
import insta_milligram.constants as ic
import insta_milligram.responses.decorators as ird
import users.models.users_follows as umuf


@ird.check_authenticated()
@ird.check_user_exists()
def delete(request: dhreq.HttpRequest, id: int, id1: int):
    requester = ag.get_auth_user(request)

    follower = dcam.User.objects.get(pk=id)
    try:
        following = dcam.User.objects.get(pk=id1)
    except dcam.User.DoesNotExist:
        return ic.responses.USER_NOT_FOUND

    if requester not in (follower, following):
        return ic.responses.OPERATION_NOT_ALLOWED

    follow = umuf.UserFollow.objects.filter(
        follower=follower,
        following=following,
    )

    if not follow.exists():
        return ic.responses.OPERATION_NOT_ALLOWED

    with ddt.atomic():
        follow.delete()
        following.profile.followers_count -= 1  # type: ignore
        follower.profile.followings_count -= 1  # type: ignore
        following.profile.save()  # type: ignore
        follower.profile.save()  # type: ignore
    return ic.responses.SUCCESS
