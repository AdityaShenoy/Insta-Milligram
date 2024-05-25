import django.contrib.auth.models as dcam
import django.db.models as ddm

from . import profiles_manager as pm


class Profile(ddm.Model):
    user = ddm.OneToOneField(
        dcam.User,
        on_delete=ddm.CASCADE,
    )
    picture = ddm.ImageField(upload_to="profile_pictures", blank=True)
    followers_count = ddm.IntegerField(default=0)
    followings_count = ddm.IntegerField(default=0)

    objects = pm.ProfileManager()
