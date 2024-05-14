import django.contrib.auth.models as dcam
import django.db.transaction as ddt
import django.http.request as dhreq

from .. import forms as f
import insta_milligram.constants as ic
import insta_milligram.forms as if_
import insta_milligram.responses.decorators as ird
import users.models.users_profiles as umup

# todo: standardize import abbreviations


@ird.check_form(f.UserForm)
def post(request: dhreq.HttpRequest):
    form_data = if_.get_data(f.UserForm(request.POST))
    existing_users_with_same_email = dcam.User.objects.filter(
        email=form_data["email"],
    )
    exisitng_users_with_same_username = dcam.User.objects.filter(
        username=form_data["username"],
    )
    if existing_users_with_same_email or exisitng_users_with_same_username:
        return ic.responses.USER_ALREADY_EXISTS
    else:
        with ddt.atomic():
            user = dcam.User.objects.create_user(**form_data)
            umup.UserProfile.objects.create(user=user)
    return ic.responses.SUCCESS
