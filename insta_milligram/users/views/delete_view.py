import django.http.request as dr
import django.contrib.auth.models as dam

import rest_framework.response as rr  # type: ignore
import rest_framework.status as rs  # type: ignore


def delete(request: dr.HttpRequest, id: int = -1):
    if id == -1:
        return rr.Response(
            {"message": "User ID Missing"},
            rs.HTTP_400_BAD_REQUEST,
        )
    try:
        dam.User.objects.get(pk=id).delete()
        return rr.Response({"message": "Success"}, rs.HTTP_200_OK)
    except dam.User.DoesNotExist:
        return rr.Response(
            {"message": "User Not Found"},
            rs.HTTP_404_NOT_FOUND,
        )
