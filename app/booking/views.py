from django.shortcuts import render, redirect
from django.contrib import messages
from . models import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from . forms import *
from django.db.models import Count
from django.db.models import Q
import random


# Create your views here.
def my_bookings(request):
    user = request.user
    if user.username:
        T = Transactions.objects.filter(user_booked=user).order_by('-start_date')
        bookings = []
        for t in T:
            g = t.rooms_allocated.all().first()
            g = GuestHouse.objects.get(id=g.guesthouse_id).name
            bookings.append({'id': t.id, 'start_date': t.start_date, 'N': t.rooms_allocated.all().__len__(), 'G': g, 'R': t.rooms_allocated.all()})
        context = {'bookings': bookings}
        return render(request, 'booking/my_bookings.html', context)
    else:
        messages.warning(request, 'You are not authorized to acces the requested page. Please Login ')
        return redirect('error')


def book(request):
    user = request.user
    # for g in ['JC Bose Guest House', 'Homi J Bhaba Guest House', 'Vikram Sarabhai Guest House']:
    #     h=0
    #     for room_type in ['Single AC', 'Double AC', 'Single Non AC', 'Double Non AC']:
    #         for i in range(h, h+11):
    #             r = Rooms()
    #             r.room_no = i
    #             r.guesthouse = GuestHouse.objects.get(name=g)
    #             r.room_type = room_type
    #             r.save()
    #         h = h+11
    # return redirect('my_bookings')
    if user.username:
        if request.method == 'POST':
            form = TransactionForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                T = Transactions.objects.filter(Q(start_date__range=(start_date, end_date)) | Q(end_date__range=(start_date, end_date)))
                R = []
                for t in T:
                    f = t.rooms_allocated.all()
                    for g in f:
                        if g.id not in R:
                            R.append(g.id)
                R = Rooms.objects.exclude(pk__in=R).values('guesthouse').annotate(rcount=Count('guesthouse'))
                context = []
                for room in R:
                    id = room.get('guesthouse')
                    guesthouse = GuestHouse.objects.get(id=room.get('guesthouse')).name
                    rcount = room.get('rcount')
                    context.append({'id': id, 'guesthouse': guesthouse, 'rcount': rcount})
                T = Transactions()
                T.start_date = start_date
                T.end_date = end_date
                T.user_booked = user
                T.save()
                return render(request, 'booking/available.html', {'rooms': context, 'T': T})
        else:
            return render(request, 'booking/index.html', {'form': TransactionForm()})
    else:
        messages.warning(request, 'You are not authorized to acces the requested page. Please Login ')
        return redirect('error')


def book_room(request, g, t):
    user = request.user
    if user.username:
        t = Transactions.objects.get(id=t)
        start_date = t.start_date
        end_date = t.end_date
        T = Transactions.objects.filter(
            Q(start_date__range=(start_date, end_date)) | Q(end_date__range=(start_date, end_date)))
        R = []
        for t in T:
            f = t.rooms_allocated.all()
            for g in f:
                if g.id not in R and g.guesthouse_id == g:
                    R.append(g.id)
        R = Rooms.objects.exclude(pk__in=R).values('id')
        R = random.choice(R)
        r = Rooms.objects.get(id=R.get('id'))
        t.rooms_allocated.add(r)
        t.save()
        return redirect('my_bookings')
    else:
        messages.warning(request, 'Requested Page Not Found ')
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