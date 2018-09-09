from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home/index.html')


def guest_house(request):
    return render(request, 'home/guest-house.html')


def guest_room(request):
    return render(request, 'home/guest-room.html')


def team(request):
    return render(request, 'home/team.html')


def admin_login(request):
    return render(request, 'home/admin-login.html')


def news(request):
    return render(request, 'home/news.html')