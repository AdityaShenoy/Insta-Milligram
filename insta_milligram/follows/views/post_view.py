import django.contrib.auth.models as dcam
import django.http.request as dhreq

import auths.get_auth_user as ag
import insta_milligram.constants.responses as icr
import insta_milligram.forms as if_
import insta_milligram.responses.decorators as ird
import follows.forms as ff
import follows.models as fm


@ird.check_authenticated()
@ird.check_user_exists()
@ird.check_authorized()
@ird.check_form(ff.UserFollowForm)
def post(request: dhreq.HttpRequest, id: int):
    follower = ag.get_auth_user(request)
    form_data = if_.get_data(ff.UserFollowForm(request.POST))

    followings = dcam.User.objects.filter(pk=form_data["user"])
    if not followings:
        return icr.USER_NOT_FOUND

    following = followings[0]
    if following == follower:
        return icr.OPERATION_NOT_ALLOWED

    is_already_following = fm.Follow.objects.filter(
        follower=follower, following=following
    ).exists()
    if is_already_following:
        return icr.OPERATION_NOT_ALLOWED

    fm.Follow.objects.create(follower=follower, following=following)
    return icr.SUCCESS
