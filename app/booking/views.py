from django.shortcuts import render, redirect
from django.contrib import messages
from . models import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from . forms import *

# Create your views here.
def my_bookings(request):
    return render(request, 'booking/my_bookings.html')


def book(request):
    if request.method == 'POST':
        startdate = request.POST['startdate']
        starttime = request.POST['starttime']
        enddate = request.POST['enddate']
        endtime = request.POST['endtime']
        people = request.POST['people']
        print(people)
    return render(request,'booking/my_bookings.html')


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


def index(request):
    return render(request, 'booking/index.html')


def account(request):
    user = request.user
    if user.username:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            mobile = request.POST['mobile']

            user.first_name = first_name
            user.last_name = last_name
            user.save()

            extended_user = ExtendedUser.objects.get(user_id=user.id)
            extended_user.mobile = mobile
            extended_user.save()

            form = UserImageForm(request.POST, request.FILES, instance=extended_user)
            if form.is_valid():
                form.save()
            messages.success(request, 'Account Updated')
            return redirect('account')
        else:
            context = {'user': user, 'extended_user': ExtendedUser.objects.get(user_id=user.id), 'image_form': UserImageForm(instance=user), 'password_form': PasswordChangeForm(request.user)}
            return render(request, 'booking/account.html', context)
    else:
        messages.warning(request, 'You are not authorized to acces the requested page. Please Login ')
        return redirect('error')


def psw_reset(request):
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)  # Important!
        messages.success(request, 'Your password was successfully updated!')
        return redirect('account')
    else:
        messages.error(request, 'Please correct the error below.')
    return redirect('account')