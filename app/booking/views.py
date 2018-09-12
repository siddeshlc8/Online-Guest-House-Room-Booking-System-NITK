from django.shortcuts import render, redirect


# Create your views here.
def book(request):
    return render(request, 'booking/book.html')


def availability(request):
    if request.method == 'POST':
        #if availabale
        return redirect('email')
        #else
        #return redirect('not_avaialable')
    else:
        return render(request, 'home/error.html')


def avaialable(request):
    return render(request, 'booking/available.html')


def not_avaialable(request):
    return render(request, 'booking/not_available.html')