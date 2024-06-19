import django.contrib.auth.models as dcam
import django.db.models as ddm
import django.db.models.query as ddmq
import django.db.transaction as ddt

import typing as t

from . import profiles_manager as pm
import follows.models as fm


class Profile(ddm.Model):
    user = ddm.OneToOneField(
        dcam.User,
        on_delete=ddm.CASCADE,
    )

    picture = ddm.ImageField(upload_to="profile_pictures", blank=True)
    bio = ddm.CharField(max_length=100, blank=True)

    followers_count = ddm.IntegerField(default=0)
    followings_count = ddm.IntegerField(default=0)

    objects = pm.ProfileManager()

    def delete(self, *args: t.Any, **kwargs: t.Any):
        with ddt.atomic():
            follows = fm.Follow.objects.filter(
                ddmq.Q(follower=self.user) | ddmq.Q(following=self.user)
            )
            for follow in follows:
                follow.delete()
            self.user.delete()
            return super().delete(*args, **kwargs)
