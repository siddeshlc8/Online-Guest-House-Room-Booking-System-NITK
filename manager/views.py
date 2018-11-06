from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate


# Create your views here.
def manager(request):
    try:
        if request.method == 'POST':
            username = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                if user.username and user.is_staff is True and user.is_superuser is False:
                    login(request, user)
                    return redirect('manager')
                else:
                    messages.warning(request, 'Email or Password does not match')
                    return redirect('login')
            else:
                messages.warning(request, 'Email or Password does not match')
                return redirect('login')
        else:
            user = request.user
            if user.username and user.is_staff is True and user.is_superuser is False:
                return render(request, 'manager/index.html')
            else:
                messages.warning(request, 'Email or Password does not match')
                return redirect('login')
    except Exception as e:
        messages.warning(request, str(e))
        return redirect('error')


def stats(request):
    try:
        if request.method == 'POST':
            username = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                if user.username and user.is_staff is True and user.is_superuser is False:
                    login(request, user)
                    return redirect('manager')
                else:
                    messages.warning(request, 'Email or Password does not match')
                    return redirect('login')
            else:
                messages.warning(request, 'Email or Password does not match')
                return redirect('login')
        else:
            user = request.user
            if user.username and user.is_staff is True and user.is_superuser is False:
                return render(request, 'manager/stats.html')
            else:
                messages.warning(request, 'Email or Password does not match')
                return redirect('login')
    except Exception as e:
        messages.warning(request, str(e))
        return redirect('error')


