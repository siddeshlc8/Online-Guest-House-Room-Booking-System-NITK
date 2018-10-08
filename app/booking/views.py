from django.shortcuts import render, redirect
from django.contrib import messages
from . models import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from . forms import *
from django.db.models import Count


# Create your views here.
def my_bookings(request):
    user = request.user
    if user.username:
        return render(request, 'booking/my_bookings.html')
    else:
        messages.warning(request, 'You are not authorized to acces the requested page. Please Login ')
        return redirect('error')


def book(request):
    user = request.user
    if user.username:
        if request.method == 'POST':
            form = TransactionForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                T = Transactions.objects.filter(start_date__gte=start_date, end_date__lte=end_date).values('room_no')
                R = Rooms.objects.exclude(pk__in=T).values('guesthouse').annotate(rcount=Count('guesthouse'))
                context = []
                for room in R:
                    guesthouse = GuestHouse.objects.get(id=room.get('guesthouse')).name
                    rcount = room.get('rcount')
                    context.append({'guesthouse': guesthouse, 'rcount': rcount})
                return render(request, 'booking/available.html', {'rooms': context})
        else:
            return render(request, 'booking/index.html', {'form': TransactionForm()})
    else:
        messages.warning(request, 'You are not authorized to acces the requested page. Please Login ')
        return redirect('error')


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
    return redirect('book')


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
        for e in form.error_messages:
            messages.error(request, e)
    return redirect('account')