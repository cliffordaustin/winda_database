"""winda_database URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user.views import GoogleLogin, FacebookLogin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/", include("user.api.urls")),
    path("api/v1/", include("lodging.api.urls")),
    path("api/v1/", include("activities.api.urls")),
    path("api/v1/", include("transport.api.urls")),
    path("api/v1/rest-auth/", include("rest_auth.urls")),
    path("api/v1/rest-auth/registration/", include("rest_auth.registration.urls")),
    path("api/v1/rest-auth/password/change/", include("rest_auth.urls")),
    path("api/v1/rest-auth/logout/", include("rest_auth.urls")),
    path("accounts/", include("allauth.urls")),
    path("auth/google/", GoogleLogin.as_view(), name="google-login"),
    path("auth/facebook/", FacebookLogin.as_view(), name="facebook-login"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
