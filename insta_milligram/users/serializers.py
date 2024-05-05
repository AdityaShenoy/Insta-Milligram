import django.contrib.auth.models as dam

import rest_framework.serializers as rsz  # type: ignore


class UserSerializer(rsz.ModelSerializer):
    class Meta:
        model = dam.User
        fields = ["username", "email", "first_name", "last_name"]
