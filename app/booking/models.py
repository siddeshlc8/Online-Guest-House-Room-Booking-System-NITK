from django.db import models
from django.contrib.auth.models import User
import os


# Create your models here.
def get_image_path(instance, filename):
    return os.path.join('users', str(instance.id), filename)


class ExtendedUser(models.Model):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE, null=False, blank=False)
    mobile = models.CharField(max_length=11, null=True)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return self.user


class GuestHouse(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Rooms(models.Model):
    room_no = models.IntegerField(null=False)
    ROOM_TYPES = [
        ('Single AC', 'Single AC'),
        ('Double AC', 'Double AC'),
        ('Single NON AC', 'Single NON AC'),
        ('Double NON AC', 'Double NON AC'),
    ]
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, null=False)
    guesthouse = models.ForeignKey(GuestHouse, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return str(self.room_no) + ' ' + self.room_type + ' ' + self.guesthouse.name


class Transactions(models.Model):
    room_no = models.ForeignKey(Rooms, on_delete=models.DO_NOTHING, null=False, blank=False)
    user_booked = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    no_people = models.IntegerField(null=True, blank=True)
