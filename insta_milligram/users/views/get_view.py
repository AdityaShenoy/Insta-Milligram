import django.http.request as dr
import django.contrib.auth.models as dam

import rest_framework.status as rs  # type: ignore

from .. import serializers as s
import insta_milligram.responses as r
import insta_milligram.responses.decorators as ird
import insta_milligram.constants as c


@ird.check_missing_id()
def get(request: dr.HttpRequest, id: int = -1):
    try:
        user = dam.User.objects.get(pk=id)
        serialized_user = s.UserSerializer(user)
        return r.create_response(
            c.messages.SUCCESS,
            rs.HTTP_200_OK,
            serialized_user.data,  # type: ignore
        )
    except dam.User.DoesNotExist:
        return c.responses.USER_NOT_FOUND
