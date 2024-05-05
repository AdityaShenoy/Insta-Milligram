import django.http.request as dr
import django.contrib.auth.models as dam

import rest_framework.response as rr  # type: ignore
import rest_framework.status as rs  # type: ignore

from .. import serializers as s


def get(request: dr.HttpRequest, id: int):
    try:
        user = dam.User.objects.get(pk=id)
        serialized_user = s.UserSerializer(user)
        return rr.Response(serialized_user.data, rs.HTTP_200_OK)
    except dam.User.DoesNotExist:
        return rr.Response(
            {"message": "User Not Found"},
            rs.HTTP_404_NOT_FOUND,
        )
