# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('get-room-message/<str:room_name>/', views.get_room_message, name="room_message"),
]