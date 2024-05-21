import django.contrib.auth.models as dcam
import django.db.transaction as ddt
import django.http.request as dhreq

import auths.get_auth_user as ag
import insta_milligram.constants as ic
import insta_milligram.forms as if_
import insta_milligram.responses.decorators as ird
import users.follows.forms as uff
import users.models.follows as umuf


@ird.check_authenticated()
@ird.check_user_exists()
@ird.check_authorized()
@ird.check_form(uff.UserFollowForm)
def post(request: dhreq.HttpRequest, id: int):
    follower = ag.get_auth_user(request)
    form_data = if_.get_data(uff.UserFollowForm(request.POST))

    followings = dcam.User.objects.filter(pk=form_data["user"])
    if not followings:
        return ic.responses.USER_NOT_FOUND

    following = followings[0]
    if following == follower:
        return ic.responses.OPERATION_NOT_ALLOWED

    is_already_following = umuf.Follow.objects.filter(
        follower=follower, following=following
    ).exists()
    if is_already_following:
        return ic.responses.OPERATION_NOT_ALLOWED

    with ddt.atomic():
        umuf.Follow.objects.create(
            follower=follower,
            following=following,
        )
        following.profile.followers_count += 1  # type: ignore
        follower.profile.followings_count += 1  # type: ignore
        following.profile.save()  # type: ignore
        follower.profile.save()  # type: ignore
    return ic.responses.SUCCESS
