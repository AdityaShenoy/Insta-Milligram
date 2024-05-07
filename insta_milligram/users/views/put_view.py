import django.http.request as dr
import django.contrib.auth.models as dam

import rest_framework.response as rr  # type: ignore
import rest_framework.status as rs  # type: ignore

from .. import forms as f


def put(request: dr.HttpRequest, id: int = -1):
    if id == -1:
        return rr.Response(
            {"message": "User ID Missing"},
            rs.HTTP_400_BAD_REQUEST,
        )
    form = f.UserForm(request.data)  # type: ignore
    if not form.is_valid():
        return rr.Response(
            {"message": "Invalid Data", "errors": form.errors},
            rs.HTTP_400_BAD_REQUEST,
        )
    form_data = form.cleaned_data
    try:
        user = dam.User.objects.get(pk=id)
        for field in form_data:
            user.__setattr__(field, form_data[field])
        user.set_password(form_data["password"])
        user.save()
        return rr.Response({"message": "Success"}, rs.HTTP_200_OK)
    except dam.User.DoesNotExist:
        return rr.Response(
            {"message": "User Does Not Exist"},
            rs.HTTP_404_NOT_FOUND,
        )
