import django.http.request as dr

import auths.views as v
import insta_milligram.constants as c


def delete(request: dr.HttpRequest, id: int = -1):
    response = v.get(request, id)
    user = response.data.get("user")  # type: ignore
    if not user:
        return response
    if user.id != id:  # type: ignore
        return c.responses.OPERATION_NOT_ALLOWED
    user.delete()  # type: ignore
    return c.responses.SUCCESS
