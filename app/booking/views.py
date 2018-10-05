from django.shortcuts import render, redirect


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
    return render(request, 'booking/account.html')