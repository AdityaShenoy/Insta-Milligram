import django.contrib.auth.models as dcam
import django.http.request as dhreq

import insta_milligram.constants as ic
import insta_milligram.forms as if_
import insta_milligram.responses.decorators as ird
import users.forms as uf
import users.models.profiles as ump


@ird.check_form(uf.UserForm)
def post(request: dhreq.HttpRequest):
    form_data = if_.get_data(uf.UserForm(request.POST))
    existing_users_with_same_email = dcam.User.objects.filter(
        email=form_data["email"],
    )
    exisitng_users_with_same_username = dcam.User.objects.filter(
        username=form_data["username"],
    )
    if existing_users_with_same_email or exisitng_users_with_same_username:
        return ic.responses.USER_ALREADY_EXISTS
    ump.Profile.objects.create(**form_data)
    return ic.responses.SUCCESS
