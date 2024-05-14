import django.contrib.auth.models as dcam
import django.db.models as ddm


class UserProfile(ddm.Model):
    user = ddm.OneToOneField(
        dcam.User,
        on_delete=ddm.CASCADE,
        related_name="profile",
    )
    followers_count = ddm.IntegerField(default=0)
    followings_count = ddm.IntegerField(default=0)
