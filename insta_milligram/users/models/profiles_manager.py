import django.contrib.auth.models as dcam
import django.db.models as ddm
import django.db.transaction as ddt

import typing as t


class ProfileManager(ddm.Manager):  # type: ignore
    def create(self, **kwargs: t.Any):  # type: ignore
        with ddt.atomic():
            user = dcam.User.objects.create_user(**kwargs)
            profile = super().create(user=user)  # type: ignore
        return profile  # type: ignore
