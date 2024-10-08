"""
URL configuration for catalogo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from ventas.views import check_referencia_photos, custom_logout_view, ver_referencias

urlpatterns = [
    path(
        "accounts/login/", LoginView.as_view(template_name="login.html"), name="login"
    ),
    path("", LoginView.as_view(template_name="login.html"), name="login"),
    path(
        "accounts/logout/",
        custom_logout_view,
        name="logout",
    ),
    path("admin/", admin.site.urls),
    path("referencias/", ver_referencias, name="ver_referencias"),
    path("check_referencia_photos/", check_referencia_photos),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
