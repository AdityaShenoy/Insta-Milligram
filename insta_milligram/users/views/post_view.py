import django.http.request as dr
import django.contrib.auth.models as dam

import rest_framework.response as rr  # type: ignore
import rest_framework.status as rs  # type: ignore

from .. import forms as f


def post(request: dr.HttpRequest):
    form = f.UserForm(request.POST)
    if not form.is_valid():
        return rr.Response(
            {"message": "Invalid Data", "errors": form.errors},
            rs.HTTP_400_BAD_REQUEST,
        )
    form_data = form.cleaned_data
    user1 = dam.User.objects.filter(email=form_data["email"])
    user2 = dam.User.objects.filter(username=form_data["username"])
    if len(user1) + len(user2):
        return rr.Response(
            {"message": "User Already Exists"},
            rs.HTTP_400_BAD_REQUEST,
        )
    else:
        dam.User.objects.create_user(**form_data)
    return rr.Response({"message": "Success"}, rs.HTTP_200_OK)
