from django.shortcuts import render, redirect
import sendgrid
import os
from sendgrid.helpers.mail import *


# Create your views here.
def my_bookings(request):
    return render(request, 'booking/my_bookings.html')


def availability(request):
    if request.method == 'POST':
         return redirect('email')
        #else
        #return redirect('not_avaialable')
    else:
        return render(request, 'home/error.html')


def avaialable(request):
    return render(request, 'booking/available.html')


def not_avaialable(request):
    return render(request, 'booking/not_available.html')


def sendEmail(request):
    send_mail('dsds','dsds','siddeshlc08@gmail.com',['siddeshlc8@gmail.com'],fail_silently=False)
    return redirect('home')


def index(request):
    return render(request, 'booking/index.html')


def account(request):
    return render(request, 'booking/account.html')