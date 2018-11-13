from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, int_to_base36, base36_to_int
from django.template.loader import render_to_string
from .token import account_activation_token
from django.contrib.auth.models import User
import sendgrid
import os
from sendgrid.helpers.mail import *
from . forms import *
from booking.forms import TransactionForm
from booking.models import ExtendedUser
import api
# Create your views here.


def sendMail(to_email, subject, content):
    sg = sendgrid.SendGridAPIClient(apikey=api.api())
    from_email = Email("siddeshlc08@gmail.com")
    print(to_email)
    to_email = Email(to_email)
    subject = subject
    content = Content("text/plain", content)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


def home(request):
    if request.user.username and request.user.is_staff is False and request.user.is_superuser is False:
        print(request.user.email)
        return redirect('index')
    return render(request, 'home/index.html', {'t_form': TransactionForm()})


def error(request):
    return render(request, 'home/error.html')


def registrer(request):
    if request.user.username and request.user.is_staff is False and request.user.is_superuser is False:
        print(request.user.email)
        return redirect('index')
    if request.method == 'GET':
        form = SignupForm()
        return render(request, 'home/register.html', {'form': form})
    elif request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if (str(email)).find('@nitk.edu.in') == -1:
                messages.success(request, ' Please Provide your institute email')
                return redirect('register')
            if User.objects.filter(email=email).__len__() is not 0:
                messages.error(request, 'User Already Exist')
                return redirect('register')
            user = form.save(commit=False)
            user.is_active = False
            user.username = form.cleaned_data.get('email')
            user.save()
            extended_user = ExtendedUser()
            extended_user.user = user
            extended_user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your NITK GHBS account.'
            message = render_to_string('home/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':  int_to_base36(user.pk),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            sendMail(to_email, mail_subject, message)
            user.is_active = False
            user.save()
            messages.success(request, ' Please go through the confirmation email sent your email')
            return redirect('register')
        else:
            messages.error(request, form.errors)
            return redirect('register')


def signin(request):
    if request.user.username and request.user.is_staff is False and request.user.is_superuser is False:
        print(request.user.email)
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('index')
        else:
            if user is not None:
                messages.warning(request, 'Please confirm your email address')
            else:
                messages.warning(request, 'Email or Password does not match')
            return redirect('login')

    return render(request, 'home/login.html')


def signout(request):
    logout(request)
    messages.success(request, 'You have  successfully logged out!')
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = base36_to_int(uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, ' Your Account has been successfully verified.')
        return redirect('index')
    else:
        return render(request, 'home/error.html', {'errors': 'Activation link is invalid!'})