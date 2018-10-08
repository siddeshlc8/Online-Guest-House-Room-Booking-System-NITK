from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ExtendedUser)
admin.site.register(GuestHouse)
admin.site.register(Rooms)