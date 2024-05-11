import django.http.request as dr

import auths.verify as v
import insta_milligram.constants as c


def delete(request: dr.HttpRequest, id: int = -1):
    response_and_user = v.verify(request, id)
    response = response_and_user.response
    if response:
        return response
    user = response_and_user.user
    if user.id != id:  # type: ignore
        return c.responses.OPERATION_NOT_ALLOWED
    user.delete()  # type: ignore
    return c.responses.SUCCESS
