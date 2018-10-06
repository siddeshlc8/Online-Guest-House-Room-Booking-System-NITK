from django import forms
from . models import ExtendedUser


class UserImageForm(forms.ModelForm):

    class Meta:
        model = ExtendedUser
        fields = [
            'image'
        ]