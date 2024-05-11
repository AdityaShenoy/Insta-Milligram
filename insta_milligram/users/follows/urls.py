import django.urls as du

from . import views as v

urlpatterns = [
    du.path("followings", v.UserFollowView.as_view(), name="users_followings"),
    # du.path("/<int:id>", v.UserFollowView.as_view(), name="users_follows_id"),
]
