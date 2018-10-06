from django.urls import path, include
from . import views

urlpatterns = [
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('email/', views.avaialable, name='email'),
    path('not-available/', views.not_avaialable, name='not_available'),
    path('availability/', views.availability, name='availability'),
    path('user/', views.index, name='index'),
    path('book/', views.book, name='book'),
    path('account/', views.account, name='account'),
    path('psw-reset/', views.psw_reset, name='psw-reset'),
]