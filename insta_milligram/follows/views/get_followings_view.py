import django.contrib.auth.models as dcam
import django.core.paginator as dcp
import django.http.request as dhreq

import insta_milligram.constants.responses as icr
import insta_milligram.responses as ir
import insta_milligram.responses.decorators as ird
import follows.models as fm
import users.serializers as us


@ird.check_authenticated()
@ird.check_user_exists()
def get(request: dhreq.HttpRequest, id: int, id1: int = -1):
    follower_id = id
    following_id = id1

    follower = dcam.User.objects.get(id=follower_id)

    if following_id == -1:
        follows = fm.Follow.objects.filter(follower=follower)
        followings = dcam.User.objects.filter(
            id__in=follows.values_list("following"),
        ).order_by("first_name", "last_name")

        paginator = dcp.Paginator(followings, 50)
        page_number = request.GET.get("page", 1)
        page = paginator.get_page(page_number)

        result = [us.UserSerializer(user).data for user in page.object_list]

        return ir.create_response(icr.SUCCESS, {"followings": result})

    try:
        following = dcam.User.objects.get(pk=following_id)
    except dcam.User.DoesNotExist:
        return icr.USER_NOT_FOUND

    is_following = follower.followings.filter(  # type: ignore
        following=following,
    ).exists()
    return ir.create_response(icr.SUCCESS, {"is_following": is_following})
