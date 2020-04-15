from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from prosocial import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

# Routers provide an easy way of automatically determining the URL conf.
ROUTER = routers.DefaultRouter()
# router.register(r"users", UserViewSet)
ROUTER.register(r"accounts", views.UserViewSet)
ROUTER.register(r"groups", views.GroupViewSet)
ROUTER.register(r"posts", views.PostViewSet)
ROUTER.register(r"comments", views.CommentViewSet)
ROUTER.register(r"reactions", views.ReactionViewSet)
ROUTER.register(r"polls", views.PollViewSet)
ROUTER.register(r"ticks", views.TickViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(ROUTER.urls)),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^api-auth/token/obtain/$", TokenObtainPairView.as_view(), name='token_obtain'),
    url(r"^api-auth/token/refresh/$", TokenRefreshView.as_view(), name='token_refresh'),
]
