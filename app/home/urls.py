from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('guest-house/', views.guest_house, name='guest_house'),
    path('guest-rooms/', views.guest_room, name='guest_room'),
    path('team/', views.team, name='team'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('news/', views.news, name='news'),
]