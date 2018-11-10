"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.manager, name='manager'),
    path('<int:id>/', views.manager1, name='manager1'),
    path('stats/', views.stats, name='stats'),
    path('account/', views.account, name='manager-account'),
    path('<int:id>/cancel/', views.cancel, name='manager-cancel'),
    path('<int:id>/<int:r>/remove', views.remove, name='manager-remove'),
    path('<int:id>/add', views.add, name='manager-add'),
    path('add-guest/<int:id>', views.add_guest, name='add_guest'),
    path('delete-guest/<int:t>/<int:id>', views.delete_guest, name='delete-guest'),
    path('booking/<int:id>/details/', views.booking_details, name='booking-details'),
]
