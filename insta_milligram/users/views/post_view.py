import django.http.request as dr
import django.contrib.auth.models as dam
import django.db.transaction as ddt

from .. import forms as f

import insta_milligram.constants as c
import insta_milligram.responses.decorators as ird
import users.models.users_profiles as umup

# todo: standardize import abbreviations


@ird.check_form(f.UserForm)
def post(request: dr.HttpRequest):
    form = f.UserForm(request.POST)
    form.is_valid()
    form_data = form.cleaned_data
    user1 = dam.User.objects.filter(email=form_data["email"])
    user2 = dam.User.objects.filter(username=form_data["username"])
    if len(user1) + len(user2):
        return c.responses.USER_ALREADY_EXISTS
    else:
        with ddt.atomic():
            user = dam.User.objects.create_user(**form_data)
            umup.UserProfile.objects.create(user=user)
    return c.responses.SUCCESS
