from django.urls import path, include
from . import views

urlpatterns = [
    path('book/', views.book, name='book'),
    path('email/', views.avaialable, name='email'),
    path('not-available/', views.not_avaialable, name='not_available'),
    path('availability/', views.availability, name='availability'),
]