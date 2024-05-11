import django.db.models as ddm
import django.contrib.auth.models as dcam


class UsersFollows(ddm.Model):
    follower = ddm.ManyToManyField(  # type: ignore
        dcam.User,
        related_name="followers",
    )
    following = ddm.ManyToManyField(  # type: ignore
        dcam.User,
        related_name="followings",
    )
