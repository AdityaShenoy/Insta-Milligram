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
    # todo: add timestamp

    def __str__(self):
        return f"{self.follower} follows {self.following}"
