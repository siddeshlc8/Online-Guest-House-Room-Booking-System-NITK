from django.shortcuts import render, redirect
import sendgrid
import os
from sendgrid.helpers.mail import *


# Create your views here.
def my_bookings(request):
    return render(request, 'booking/my_bookings.html')


def availability(request):
    if request.method == 'POST':
        # sg = sendgrid.SendGridAPIClient(apikey='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')
        # from_email = Email("siddeshlc08@gmail.com")
        # to_email = Email("siddeshlc8@gmail.com")
        # subject = "Sending with SendGrid is Fun"
        # content = Content("text/plain", "and easy to do anywhere, even with Python")
        # mail = Mail(from_email, subject, to_email, content)
        # response = sg.client.mail.send.post(request_body=mail.get())
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
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