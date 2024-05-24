import django.contrib.auth.models as dcam

import rest_framework_simplejwt.tokens as jt

import insta_milligram.constants.inputs as ici
import users.models.profiles as ump


def signup_and_login(id: int):
    signup_request = ici.signup_request(id)
    try:
        user = dcam.User.objects.get(username=signup_request["username"])
    except dcam.User.DoesNotExist:
        user = ump.Profile.objects.create(**signup_request).user
    access_token = jt.AccessToken.for_user(user)
    return {"Authorization": f"Bearer {access_token}"}
