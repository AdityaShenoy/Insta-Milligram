"""
URL configuration for insta_milligram project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import django.conf as dc
import django.conf.urls.static as dcus
import django.contrib.admin as dca
import django.urls as du

urlpatterns = [
    du.path("admin", dca.site.urls),
    du.path("users", du.include("users.urls")),
    du.path("auths", du.include("auths.urls")),
    du.path("users/<int:id>/", du.include("users.follows.urls")),
]

if dc.settings.DEBUG:
    urlpatterns += dcus.static(
        dc.settings.MEDIA_URL, document_root=dc.settings.MEDIA_ROOT
    )
