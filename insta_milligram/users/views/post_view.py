import django.http.request as dr
import django.contrib.auth.models as dam

import rest_framework.status as rs  # type: ignore

from .. import forms as f

import insta_milligram.constants as c
import insta_milligram.helpers as h


def post(request: dr.HttpRequest):
    form = f.UserForm(request.POST)
    if not form.is_valid():
        return h.create_response(
            c.messages.INVALID_DATA,
            rs.HTTP_400_BAD_REQUEST,
            {"errors": form.errors},
        )
    form_data = form.cleaned_data
    user1 = dam.User.objects.filter(email=form_data["email"])
    user2 = dam.User.objects.filter(username=form_data["username"])
    if len(user1) + len(user2):
        return c.responses.USER_ALREADY_EXISTS
    else:
        dam.User.objects.create_user(**form_data)
    return c.responses.SUCCESS
