import django.contrib.auth.models as dcam

import rest_framework.serializers as rsz  # type: ignore


class UserSerializer(rsz.ModelSerializer):
    class Meta:
        model = dcam.User
        fields = ["id", "username", "email", "first_name", "last_name"]
