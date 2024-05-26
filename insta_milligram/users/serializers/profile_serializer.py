import rest_framework.serializers as rsz  # type: ignore

import users.models.profiles as ump


class ProfileSerializer(rsz.ModelSerializer):
    class Meta:
        model = ump.Profile
        exclude = ["user"]
