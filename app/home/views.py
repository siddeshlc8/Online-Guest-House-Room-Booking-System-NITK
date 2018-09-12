from django.shortcuts import render, redirect

# Create your views here.


def home(request):
    return render(request, 'home/index.html')


def error(request):
    return render(request, 'home/error.html')




