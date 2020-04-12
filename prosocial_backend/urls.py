from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from prosocial import views

# Routers provide an easy way of automatically determining the URL conf.
ROUTER = routers.DefaultRouter()
# router.register(r"users", UserViewSet)
ROUTER.register(r"accounts", views.AccountViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(ROUTER.urls)),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
