from django.db import models
from django.contrib.auth.models import User
import os


# Create your models here.
def get_image_path(instance, filename):
    return os.path.join('users', str(instance.id), filename)


class ExtendedUser(models.Model):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE, null=False, blank=False)
    mobile = models.CharField(max_length=11, null=True)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True, default='users/no.png')

    if user:
        def __str__(self):
            return str(self.user)


class GuestHouse(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    code = models.CharField(max_length=3, null=True, unique=True)
    next_transaction_number = models.IntegerField(default=0, null=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Rooms(models.Model):
    room_no = models.IntegerField(null=False)
    ROOM_TYPES = [
        ('Single-AC', 'Single-AC'),
        ('Double-AC', 'Double-AC'),
        ('Single-NON-AC', 'Single NON-AC'),
        ('Double-NON-AC', 'Double-NON-AC'),
    ]
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, null=False)
    guesthouse = models.ForeignKey(GuestHouse, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return str(self.room_no) + ' ' + self.room_type + ' ' + self.guesthouse.name


class Transactions(models.Model):
    transaction_number = models.CharField(max_length=10, null=True)
    user_booked = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    no_people = models.IntegerField(null=True, blank=True)
    no_rooms = models.IntegerField(null=True, blank=True)
    rooms_allocated = models.ManyToManyField('Rooms')
    status = models.BooleanField(default=False)
    guesthouse = models.ForeignKey(GuestHouse, on_delete=models.CASCADE, null=True, blank=True)
    date_book = models.DateField(null=True, blank=True)
    ROOM_TYPES = [
        ('Single-AC', 'Single-AC'),
        ('Double-AC', 'Double-AC'),
        ('Single-NON-AC', 'Single NON-AC'),
        ('Double-NON-AC', 'Double-NON-AC'),
    ]

    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, null=True, blank=True)

    def __str__(self):
        return self.transaction_number


class PreTransactions(models.Model):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    no_people = models.IntegerField(null=True, blank=True)
    no_people_done = models.IntegerField(null=True, blank=True,default=0)
    no_rooms = models.IntegerField(null=True, blank=True)
    guesthouse = models.ForeignKey(GuestHouse, on_delete=models.CASCADE, null=True, blank=True)
    ROOM_TYPES = [
        ('Single-AC', 'Single-AC'),
        ('Double-AC', 'Double-AC'),
        ('Single-NON-AC', 'Single NON-AC'),
        ('Double-NON-AC', 'Double-NON-AC'),
    ]

    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, null=True, blank=True)

    def __str__(self):
        return str(self.guesthouse) + ' || ' + str(self.start_date) + ' - ' + str(self.end_date)


class GuestDetails(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    transaction = models.ForeignKey(Transactions, on_delete=models.CASCADE, null=True, blank=True)