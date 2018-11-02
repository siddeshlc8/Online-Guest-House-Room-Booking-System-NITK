from django.shortcuts import render, redirect


# Create your views here.
def admin(request):
    user = request.user
    #if user.username and user.is_staff is True and user.is_superuser is False:
    return render(request, 'administrator/admin.html')