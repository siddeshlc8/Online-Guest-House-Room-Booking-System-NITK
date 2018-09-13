from django.urls import path, include
from . import views

urlpatterns = [
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('email/', views.avaialable, name='email'),
    path('not-available/', views.not_avaialable, name='not_available'),
    path('availability/', views.availability, name='availability'),
    path('send-email/', views.sendEmail, name='sendEmail'),
    path('user/', views.index, name='index'),
    path('account/', views.account, name='account'),
]