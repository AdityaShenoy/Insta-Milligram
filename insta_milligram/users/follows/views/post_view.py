import django.contrib.auth.models as dcam
import django.db.transaction as ddt
import django.http.request as dhreq

import auths.get_auth_user as ag
import insta_milligram.constants as ic
import insta_milligram.forms as if_
import insta_milligram.responses.decorators as ird
import users.follows.forms as uff
import users.models.users_follows as umuf


@ird.check_authenticated()
@ird.check_user_exists()
@ird.check_form(uff.UserFollowForm)
def post(request: dhreq.HttpRequest, id: int):
    user = ag.get_auth_user(request)
    form_data = if_.get_data(uff.UserFollowForm(request.POST))
    followed_users = dcam.User.objects.filter(pk=form_data["user"])
    if not followed_users:
        return ic.responses.USER_NOT_FOUND
    followed_user = followed_users[0]
    if followed_user == user:
        return ic.responses.OPERATION_NOT_ALLOWED

    is_already_following = umuf.UserFollow.objects.filter(
        follower=user, following=followed_user
    ).exists()
    if is_already_following:
        return ic.responses.OPERATION_NOT_ALLOWED

    with ddt.atomic():
        umuf.UserFollow.objects.create(
            follower=user,
            following=followed_user,
        )
        followed_user.profile.followers_count += 1  # type: ignore
        user.profile.followings_count += 1  # type: ignore
        followed_user.profile.save()  # type: ignore
        user.profile.save()  # type: ignore
    return ic.responses.SUCCESS
