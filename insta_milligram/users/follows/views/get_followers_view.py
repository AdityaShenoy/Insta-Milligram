import django.contrib.auth.models as dcam
import django.core.paginator as dcp
import django.http.request as dhreq

import insta_milligram.constants.responses as icr
import insta_milligram.responses as ir
import insta_milligram.responses.decorators as ird
import users.models.follows as umuf
import users.serializers as us


@ird.check_authenticated()
@ird.check_user_exists()
def get_followers(request: dhreq.HttpRequest, id: int):
    following = dcam.User.objects.get(pk=id)

    follows = umuf.Follow.objects.filter(following=following)

    followers = dcam.User.objects.filter(
        id__in=follows.values_list("follower")
    ).order_by("first_name", "last_name")

    paginator = dcp.Paginator(followers, 50)
    page_number = request.GET.get("page", 1)
    page = paginator.get_page(page_number)

    result = [us.UserSerializer(user).data for user in page.object_list]
    return ir.create_response(icr.SUCCESS, {"followers": result})
