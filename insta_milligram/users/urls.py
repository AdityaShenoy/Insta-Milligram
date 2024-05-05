import django.urls as du

from . import views as v

urlpatterns = [du.path("", v.UserView.as_view(), name="users")]
