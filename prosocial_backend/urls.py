from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from rest_framework import routers

from prosocial import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
ROUTER.register(r"notifications", views.NotificationViewSet, basename="notifications")
ROUTER.register(r"newsfeed", views.NewsFeedViewSet, basename="newsfeed")
ROUTER.register(r"notificationmember", views.NotificationMemberViewSet, basename='notificationmember')



urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include(ROUTER.urls)),
        path("auth/", include("djoser.urls")),
        path("auth/", include("djoser.urls.jwt")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.FRONTEND_URL, document_root=settings.FRONTEND_ROOT)
)
