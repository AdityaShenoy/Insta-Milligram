import django.http.request as dr

import rest_framework.response as rr  # type: ignore
import rest_framework.status as rs  # type: ignore


import auths.verify as v


def delete(request: dr.HttpRequest, id: int = -1):
    response_and_user = v.verify(request, id)
    response = response_and_user.response
    if response:
        return response
    user = response_and_user.user
    if user.id != id:  # type: ignore
        return rr.Response(
            {"message": "Operation Not Allowed"},
            rs.HTTP_403_FORBIDDEN,
        )
    user.delete()  # type: ignore
    return rr.Response({"message": "Success"}, rs.HTTP_200_OK)
