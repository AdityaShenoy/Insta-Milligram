import django.contrib.auth.models as dcam
import django.db.models as ddm
import django.db.transaction as ddt

import typing as t

from . import follows_manager as fm


class Follow(ddm.Model):
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

    objects = fm.FollowManager()

    def __str__(self):
        return f"{self.follower} follows {self.following}"

    def delete(self, *args: t.Any, **kwargs: t.Any):
        with ddt.atomic():
            self.follower.profile.followings_count -= 1  # type: ignore
            self.following.profile.followers_count -= 1  # type: ignore
            self.follower.profile.save()  # type: ignore
            self.following.profile.save()  # type: ignore
            return super().delete(*args, **kwargs)
