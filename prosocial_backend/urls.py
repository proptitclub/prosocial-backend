from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers

from prosocial import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
import chat.views as chat_views

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
ROUTER.register(r"point", views.PointViewSet, basename='point')
ROUTER.register(r'bonuspoint', views.BonusPointViewSet, basename='bonuspoint')
ROUTER.register(r'target', views.TargetViewSet, basename='target')

ROUTER_CHAT = routers.DefaultRouter()
ROUTER_CHAT.register(r"rooms", chat_views.RoomViewSet)

api_info = openapi.Info(
    title="Snippets API",
    default_version='v1',
    description="Test description",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="contact@snippets.local"),
    license=openapi.License(name="BSD License"),
)


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_services="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD Licence")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include(ROUTER.urls)),
        path("chat-api/", include(ROUTER_CHAT.urls)),
        path("rank/", views.get_rank, name="rank-json"),
        path("device/create", views.create_device_member, name="create_device"),
        path("device/delete", views.delete_device_member, name="delete_device"),
        path("test/testnoti", views.test_noti, name="testnoti"),
        path("lixi/get", views.gen_lixi, name="genlixi"),
        # path("lixi/get", views.get_lixi, name="getlixi"),
        path("auth/", include("djoser.urls")),
        path("auth/", include("djoser.urls.jwt")),
        path("users/create/", views.create_user),
        path("posts2/create/", views.create_post),
        url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path("chat/", include('chat.urls')),
        path("convert/", views.convert_first_last_name, name='convertname'),
        path("users/block/", views.block_user, name='block'),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.FRONTEND_URL, document_root=settings.FRONTEND_ROOT)
)
