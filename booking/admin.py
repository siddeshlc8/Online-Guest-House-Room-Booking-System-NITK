from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ExtendedUser)
admin.site.register(GuestHouse)
admin.site.register(Rooms)
admin.site.register(Transactions)
admin.site.register(PreTransactions)
admin.site.register(GuestDetails)