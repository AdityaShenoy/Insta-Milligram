import django.http.request as dr
import django.contrib.auth.models as dam

import rest_framework.response as rr  # type: ignore
import rest_framework.status as rs  # type: ignore

import rest_framework_simplejwt.tokens as jt

from ... import forms as f


def generate_tokens(request: dr.HttpRequest):
    form = f.GenerateTokenForm(request.POST)
    if not form.is_valid():
        return rr.Response(
            {"message": "Invalid Data", "errors": form.errors},
            rs.HTTP_400_BAD_REQUEST,
        )
    form_data = form.cleaned_data
    try:
        user = dam.User.objects.get(username=form_data["username"])
        if not user.check_password(form_data["password"]):
            return rr.Response(
                {"message": "Incorrect Password"}, rs.HTTP_401_UNAUTHORIZED
            )
        refresh_token = jt.RefreshToken.for_user(user)
        access_token = refresh_token.access_token  # type: ignore
        return rr.Response(
            {
                "message": "Success",
                "tokens": {
                    "refresh": str(refresh_token),
                    "access": str(access_token),  # type: ignore
                },
            },
            rs.HTTP_200_OK,
        )
    except dam.User.DoesNotExist:
        return rr.Response(
            {"message": "User Not Found"},
            rs.HTTP_401_UNAUTHORIZED,
        )
