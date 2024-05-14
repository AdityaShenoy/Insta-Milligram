import django.http.request as dhreq

import auths.views as av
import insta_milligram.constants as ic
import insta_milligram.responses.decorators as ird


@ird.check_missing_id()
def delete(request: dhreq.HttpRequest, id: int = -1):
    response = av.get(request, id)
    user = response.data.get("user")  # type: ignore
    if not user:
        return response
    if user.id != id:  # type: ignore
        return ic.responses.OPERATION_NOT_ALLOWED
    user.delete()  # type: ignore
    return ic.responses.SUCCESS
