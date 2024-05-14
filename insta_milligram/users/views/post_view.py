import django.http.request as dhreq
import django.contrib.auth.models as dcam
import django.db.transaction as ddt

from .. import forms as f

import insta_milligram.constants as ic
import insta_milligram.responses.decorators as ird
import insta_milligram.forms as if_
import users.models.users_profiles as umup

# todo: standardize import abbreviations


@ird.check_form(f.UserForm)
def post(request: dhreq.HttpRequest):
    form_data = if_.get_data(f.UserForm(request.POST))
    user1 = dcam.User.objects.filter(email=form_data["email"])
    user2 = dcam.User.objects.filter(username=form_data["username"])
    if len(user1) + len(user2):
        return ic.responses.USER_ALREADY_EXISTS
    else:
        with ddt.atomic():
            user = dcam.User.objects.create_user(**form_data)
            umup.UserProfile.objects.create(user=user)
    return ic.responses.SUCCESS
