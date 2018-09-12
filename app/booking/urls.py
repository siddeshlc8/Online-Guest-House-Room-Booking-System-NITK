from django.urls import path, include
from . import views

urlpatterns = [
    path('book/', views.book, name='book'),
]