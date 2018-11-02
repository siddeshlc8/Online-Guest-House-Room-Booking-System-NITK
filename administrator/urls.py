from django.urls import path
from administrator import views

urlpatterns = [
    path('', views.admin, name='admin'),
]