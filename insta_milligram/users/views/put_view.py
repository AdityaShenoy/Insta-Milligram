import django.http.request as dr
import django.contrib.auth.models as dam

import rest_framework.status as rs  # type: ignore

from .. import forms as f
import insta_milligram.constants as c
import insta_milligram.responses as r


def put(request: dr.HttpRequest, id: int = -1):
    if id == -1:
        return c.responses.USER_ID_MISSING
    form = f.UserForm(request.data)  # type: ignore
    if not form.is_valid():
        return r.create_response(
            c.messages.INVALID_DATA,
            rs.HTTP_400_BAD_REQUEST,
            {"errors": form.errors},
        )
    form_data = form.cleaned_data
    try:
        user = dam.User.objects.get(pk=id)
        for field in form_data:
            user.__setattr__(field, form_data[field])
        user.set_password(form_data["password"])
        user.save()
        return c.responses.SUCCESS
    except dam.User.DoesNotExist:
        return c.responses.USER_NOT_FOUND
