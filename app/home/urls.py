from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('error/', views.error, name='error'),
    path('booking/', include('booking.urls')),
]