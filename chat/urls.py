# chat/urls.py
from django.urls import path

from . import views
from rest_framework import routers
from django.urls import path, include

ROUTER_CHAT = routers.DefaultRouter()
ROUTER_CHAT.register(r"rooms", views.RoomViewSet)

urlpatterns = [
    path('messages/<str:room_name>/', views.get_room_message, name="room_message"),
    path("", include(ROUTER_CHAT.urls)),
]