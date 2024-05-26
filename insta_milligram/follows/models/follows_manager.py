import django.db.models as ddm
import django.db.transaction as ddt

import typing as t


class FollowManager(ddm.Manager):  # type: ignore
    def create(self, **kwargs: t.Any):  # type: ignore
        with ddt.atomic():
            follow = super().create(**kwargs)  # type: ignore
            follower = kwargs["follower"]
            following = kwargs["following"]
            following.profile.followers_count += 1
            follower.profile.followings_count += 1
            following.profile.save()
            follower.profile.save()
        return follow  # type: ignore
