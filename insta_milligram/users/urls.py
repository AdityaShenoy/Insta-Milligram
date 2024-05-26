import django.urls as du

from . import views as v

urlpatterns = [
    du.path(
        "",
        v.UserView.as_view(),
        name="users",
    ),
    du.path(
        "/<int:id>",
        v.UserView.as_view(),
        name="users_id",
    ),
    du.path(
        "/<int:id>/profile",
        v.UserProfileView.as_view(),
        name="users_profile",
    ),
]
