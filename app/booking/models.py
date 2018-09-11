from django.db import models


# Create your models here.
class GuestHouse(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    active = models.BooleanField(default=True)
