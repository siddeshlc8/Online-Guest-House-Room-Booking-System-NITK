from django.urls import path, include
from . import views

urlpatterns = [
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('availability/', views.availability, name='availability'),
    path('user/', views.index, name='index'),
    path('book/<int:t>/', views.book, name='book'),
    path('account/', views.account, name='account'),
    path('psw-reset/', views.psw_reset, name='psw-reset'),
    path('book/<int:g>/<int:t>/<slug:rtype>/<int:count>/', views.book_room_verify, name='book_room_verify'),
]