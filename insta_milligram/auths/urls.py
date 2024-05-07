import django.urls as du

from . import views as v

urlpatterns = [
    du.path("", v.AuthView.as_view(), name="auths"),
]
