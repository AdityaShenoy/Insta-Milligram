import django.urls as du

from . import views as v

urlpatterns = [
    du.path(
        "followings",
        v.UserFollowView.as_view(),
        name="users_followings",
    ),
    du.path(
        "followings/<int:id1>",
        v.UserFollowView.as_view(),
        name="users_followings",
    ),
    du.path(
        "followers",
        v.UserFollowerView.as_view(),
        name="users_followers",
    ),
]
