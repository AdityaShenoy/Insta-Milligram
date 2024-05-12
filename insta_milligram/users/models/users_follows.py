import django.db.models as ddm
import django.contrib.auth.models as dcam


class UserFollow(ddm.Model):
    follower = ddm.ForeignKey(  # type: ignore
        dcam.User,
        on_delete=ddm.CASCADE,
        related_name="followings",
    )
    following = ddm.ForeignKey(  # type: ignore
        dcam.User,
        on_delete=ddm.CASCADE,
        related_name="followers",
    )
