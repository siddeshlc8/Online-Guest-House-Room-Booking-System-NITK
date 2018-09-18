from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.


def home(request):
    return render(request, 'home/index.html')


def error(request):
    return render(request, 'home/error.html')


def registrer(request):
    if request.method == 'GET':
        return render(request, 'home/register.html')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        rpt_password = request.POST['rpt-password']
        errors = 0
        if password != rpt_password:
            errors=1
            messages.warning(request, 'Passwords don not match')

        if 'nitk.edu.in' not in email:
            errors = 1
            messages.warning(request, 'Please enter institute email address')

        if errors ==1:
            return redirect('register')

        return render(request, 'home/index.html')


def login(request):
    return render(request, 'home/login.html')