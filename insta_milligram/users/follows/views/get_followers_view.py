import django.contrib.auth.models as dcam
import django.http.request as dhreq

import insta_milligram.constants as ic
import insta_milligram.responses as ir
import insta_milligram.responses.decorators as ird


@ird.check_authenticated()
@ird.check_user_exists()
def get_followers(request: dhreq.HttpRequest, id: int):
    following = dcam.User.objects.get(pk=id)
    # todo: paginate the users list instead of sending user ids
    followers = following.followers.all().values_list(  # type: ignore
        "follower",
        flat=True,
    )
    return ir.create_response(ic.responses.SUCCESS, {"followers": followers})
