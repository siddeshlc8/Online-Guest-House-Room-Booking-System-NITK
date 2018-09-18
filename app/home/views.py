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
from sendgrid.helpers.mail import *
from . forms import *
# Create your views here.


def sendMail(to_email, subject, content):
    sg = sendgrid.SendGridAPIClient(apikey='**************')
    from_email = Email("siddeshlc08@gmail.com")
    to_email = Email(to_email)
    subject = subject
    content = Content("text/plain", content)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


def home(request):
    return render(request, 'home/index.html')


def error(request):
    return render(request, 'home/error.html')


def registrer(request):
    if request.method == 'GET':
        form = SignupForm()
        return render(request, 'home/register.html', {'form': form})
    elif request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.username = form.cleaned_data.get('email')
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('home/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':  int_to_base36(user.pk),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            sendMail(to_email, mail_subject, message)
            messages.success(request, 'Registration success full.Please confirm your email to proceed')
            return redirect('register')
        else:
            messages.error(request, 'Error')
            return redirect('register')


def signin(request):
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
    #messages.success(request, 'You have  successfully logged out!')
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
        return redirect('index')
    else:
        return render(request, 'home/error.html', {'errors': 'Activation link is invalid!'})