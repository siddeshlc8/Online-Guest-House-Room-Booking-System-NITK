from django.shortcuts import render, redirect
from django.contrib import messages
from . models import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from . forms import *
from django.db.models import Count
from django.db.models import Q
import random, itertools, datetime
from django.template.loader import render_to_string
from home.views import sendMail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sites.shortcuts import get_current_site


def index(request):
    try:
        user = request.user
        if user.username and user.is_staff is False and user.is_superuser is False:
            if request.method == 'POST':
                form = TransactionForm(request.POST)
                if form.is_valid():
                    start_date = form.cleaned_data['start_date']
                    end_date = form.cleaned_data['end_date']
                    if start_date > end_date or start_date < datetime.date.today():
                        messages.warning(request, 'Please Enter Proper dates')
                        return redirect('index')
                    T = PreTransactions()
                    T.start_date = start_date
                    T.end_date = end_date
                    T.save()
                    return redirect('book', T.id)
                else:
                    for e in form.errors:
                        messages.error(request, e)
                    return redirect('index')
            else:
                return render(request, 'booking/index.html', {'form': TransactionForm()})
        else:
            return redirect('home')
    except Exception as e:
        messages.warning(request, str(e))
        return redirect('error')


def book(request, t):
    try:
        user = request.user
        if user.username and user.is_staff is False and user.is_superuser is False:
            if request.method == 'POST':
                return redirect('index')
            else:
                tt = PreTransactions.objects.get(id=t)
                start_date = tt.start_date
                end_date = tt.end_date
                T = Transactions.objects.filter(
                    Q(start_date__range=(start_date, end_date)) | Q(end_date__range=(start_date, end_date))).filter(status=True)
                R = []
                for t in T:
                    f = t.rooms_allocated.all()
                    for g in f:
                        if g.id not in R:
                            R.append(g.id)
                G = GuestHouse.objects.all()
                context = []
                for g in G:
                    rooms_available = Rooms.objects.exclude(pk__in=R).filter(guesthouse_id=g.id).values(
                        'room_type').annotate(count=Count('room_type'))
                    no_rooms = 0
                    rooms = []
                    for room in rooms_available:
                        types = str(room.get('room_type'))
                        count = room.get('count')
                        form = NoGuestsRoomForm(count, types)
                        rooms.append({'type': types, 'count': count, 'form': form})
                        no_rooms = no_rooms + count
                    context.append({'G': g, 'no_rooms': no_rooms, 'rooms': rooms})
                return render(request, 'booking/available.html', {'rooms': context, 'T': tt})
        else:
            messages.warning(request, ' Page Not Found ')
            return redirect('home')
    except Exception as e:
        messages.warning(request, 'Something Went Wrong. Please Try agin')
        return redirect('index')


def book_room_verify(request, g, t, rtype, count):
    try:
        user = request.user
        if user.username and user.is_staff is False and user.is_superuser is False:
            if request.method == 'POST':
                form = NoGuestsRoomForm(count, rtype, request.POST)
                if form.is_valid():
                    no_g = form.cleaned_data['no_guests']
                    no_r = form.cleaned_data['no_rooms']
                    no_guests = 0
                    if rtype == 'Single-AC':
                        no_guests = no_r
                    elif rtype == 'Single-Non-AC':
                        no_guests = no_r
                    elif rtype == 'Double-AC':
                        no_guests = no_r * 2
                    elif rtype == 'Double-Non-AC':
                        no_guests = no_r * 2
                    if no_g > no_guests:
                        messages.warning(request, 'Sorry ' + str(no_g) + ' guests ' + 'can not fit in ' + str(no_r) + ' rooms')
                        return redirect('book', t)
                    T = PreTransactions.objects.get(id=t)
                    T.room_type = rtype
                    T.no_people = no_g
                    T.no_rooms = no_r
                    T.save()
                    newtransaction = book_room(g, t, request)
                    if newtransaction is not False:

                        mail_subject = 'Booking Confirmation at NITK GuestHouse.'
                        message = render_to_string('booking/booking_confirmation.html', {
                            'user': request.user,
                            'newtransaction': newtransaction,
                            'rooms': newtransaction.rooms_allocated.all()
                        })
                        to_email = request.user.email
                        #sendMail(to_email, mail_subject, message)
                        messages.warning(request, 'Your Booking is Succesfull. Please Pay the amout While Checking In')
                        return redirect('my_bookings')
                    else:
                        messages.warning(request, 'Some thing went wrong book again ')
                        return redirect('index')
                else:
                    messages.warning(request, 'Requested Page Not Found ')
                    return redirect('error')
            else:
                messages.warning(request, 'Requested Page Not Found ')
                return redirect('error')
        else:
            messages.warning(request, 'Requested Page Not Found ')
            return redirect('home')
    except Exception as e:
        messages.warning(request, 'Something Went Wrong. Please Try agin')
        return redirect('index')


def book_room(g, t, request):
    t = PreTransactions.objects.get(id=t)
    rtype = t.room_type
    t.guesthouse = GuestHouse.objects.get(id=g)
    t.save()
    start_date = t.start_date
    end_date = t.end_date
    T = Transactions.objects.filter(
        Q(start_date__range=(start_date, end_date)) | Q(end_date__range=(start_date, end_date))).filter(status=True)
    R = []
    print(GuestHouse.objects.get(id=g))
    for d in T:
        f = d.rooms_allocated.all().filter(guesthouse=d.guesthouse).filter(room_type=rtype)
        for g in f:
            if g.id not in R:
                R.append(g.id)
    R = Rooms.objects.filter(guesthouse=t.guesthouse).filter(room_type=rtype).order_by('room_no').exclude(pk__in=R).values('id')[:t.no_rooms]
    if R.__len__() == 0:
        t.delete()
        return False

    newtransaction = Transactions()
    length = (str(t.guesthouse.code) + str(t.guesthouse.next_transaction_number)).__len__()
    z = ''
    while True:
        if 10 - length == 0:
            break
        z = z + str(0)
        length = length + 1
    newtransaction.transaction_number = str(t.guesthouse.code) + z + str(t.guesthouse.next_transaction_number)
    newtransaction.start_date = start_date
    newtransaction.end_date = end_date
    newtransaction.user_booked = request.user
    newtransaction.date_book = datetime.date.today()
    newtransaction.no_people = t.no_people
    newtransaction.no_rooms = t.no_rooms
    newtransaction.guesthouse = t.guesthouse
    newtransaction.status = True
    newtransaction.room_type = t.room_type
    newtransaction.save()

    for r in R:
        room = Rooms.objects.get(id=r.get('id'))
        newtransaction.rooms_allocated.add(room)
    newtransaction.save()
    t.guesthouse.next_transaction_number = t.guesthouse.next_transaction_number + 1
    t.guesthouse.save()
    t.delete()

    return newtransaction


def my_bookings(request):
    try:
        user = request.user
        if user.username and user.is_staff is False and user.is_superuser is False:
            T = Transactions.objects.filter(user_booked=user).order_by('-date_book')
            bookings = []
            page = request.GET.get('page', 1)
            paginator = Paginator(T, 3)
            try:
                T = paginator.page(page)
            except PageNotAnInteger:
                T = paginator.page(1)
            except EmptyPage:
                T = paginator.page(paginator.num_pages)
            for t in T:
                g = t.guesthouse
                d = GuestDetails.objects.filter(transaction=t.id)
                r = t.rooms_allocated.all()
                z = itertools.zip_longest(d, r)
                bookings.append({'T': t, 'N': r.__len__(), 'G': g, 'Z': z})
            context = {'bookings': bookings, 't': T}
            return render(request, 'booking/my_bookings.html', context)
        else:
            messages.warning(request, 'You are not authorized to acces the requested page. Please Login ')
            return redirect('home')
    except Exception as e:
        messages.warning(request, str(e))
        return redirect('error')


def account(request):
    try:
        user = request.user
        if user.username and user.is_staff is False and user.is_superuser is False:
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
            return redirect('home')
    except Exception as e:
        messages.warning(request, str(e))
        return redirect('error')


def psw_reset(request):
    try:
        user = request.user
        if user.username and user.is_staff is False and user.is_superuser is False:
            if request.method == 'POST':
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
            else:
                messages.warning(request, 'You are not authorized to acces the requested page. Please Login ')
                return redirect('error')
        else:
            messages.warning(request, 'You are not authorized to acces the requested page. Please Login ')
            return redirect('home')
    except Exception as e:
        messages.warning(request, str(e))
        return redirect('error')


def availability(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            if start_date > end_date or start_date < datetime.date.today():
                messages.warning(request, 'Please Enter Proper dates')
                return redirect('home')
            T = Transactions.objects.filter(
                Q(start_date__range=(start_date, end_date)) | Q(end_date__range=(start_date, end_date)))
            R = []
            for t in T:
                f = t.rooms_allocated.all()
                for g in f:
                    if g.id not in R:
                        R.append(g.id)
            G = GuestHouse.objects.all()
            context = []
            for g in G:
                rooms_available = Rooms.objects.exclude(pk__in=R).filter(guesthouse_id=g.id).values(
                    'room_type').annotate(count=Count('room_type'))
                no_rooms = 0
                rooms = []
                for room in rooms_available:
                    types = str(room.get('room_type'))
                    count = room.get('count')
                    form = NoGuestsRoomForm(count, types)
                    rooms.append({'type': types, 'count': count, 'form': form})
                    no_rooms = no_rooms + count
                context.append({'G': g, 'no_rooms': no_rooms, 'rooms': rooms})
            return render(request, 'booking/availability.html', {'rooms': context})
        else:
            messages.warning(request, 'Requested Page Not Found ')
            return redirect('index')
    else:
        return render(request, 'home/error.html')


def cancel(request, id):
    try:
        if request.method == 'POST':
            return redirect('my_bookings')
        else:
            user = request.user
            if user.username and user.is_staff is False and user.is_superuser is False:
                transaction = Transactions.objects.get(id=id)
                transaction.status = False
                transaction.save()
                mail_subject = 'Booking Cancellation at NITK GuestHouse.'
                message = render_to_string('booking/booking_cancel.html', {
                    'user': request.user,
                    'newtransaction': transaction,
                    'rooms': transaction.rooms_allocated.all(),
                    'domain': get_current_site(request).domain
                })
                to_email = request.user.email
                #sendMail(to_email, mail_subject, message)
                messages.warning(request, 'Your Booking with Booking number  ' + str(transaction.transaction_number) + ' is cancelled Succesfully')
                return redirect('my_bookings')
            else:
                messages.warning(request, 'Email or Password does not match')
                return redirect('login')
    except Exception as e:
        messages.warning(request, str(e))
        return redirect('error')


    # for g in ['JC Bose Guest House', 'Homi J Bhaba Guest House', 'Vikram Sarabhai Guest House']:
    #     h=1
    #     for room_type in ['Single-AC', 'Double-AC', 'Single-Non-AC', 'Double-Non-AC']:
    #         for i in range(h, h+10):
    #             r = Rooms()
    #             r.room_no = i
    #             r.guesthouse = GuestHouse.objects.get(name=g)
    #             r.room_type = room_type
    #             r.save()
    #         h = h+10
    # return redirect('my_bookings')