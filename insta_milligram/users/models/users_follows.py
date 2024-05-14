import django.contrib.auth.models as dcam
import django.db.models as ddm


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
    at = ddm.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.follower} follows {self.following}"
