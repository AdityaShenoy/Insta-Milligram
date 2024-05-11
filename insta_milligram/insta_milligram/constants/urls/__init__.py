import django.urls as du

USERS = du.reverse("users")
USERS_ID_1 = du.reverse("users_id", args=[1])
USERS_ID_2 = du.reverse("users_id", args=[2])
AUTHS = du.reverse("auths")
