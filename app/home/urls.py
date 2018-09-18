from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('error/', views.error, name='error'),
    path('booking/', include('booking.urls')),
    path('register/', views.registrer, name='register'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path("activate/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/",
        views.activate, name='activate'),
]