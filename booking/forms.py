from django import forms
from . models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class UserImageForm(forms.ModelForm):

    class Meta:
        model = ExtendedUser
        fields = [
            'image'
        ]


class TransactionForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=True)
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=True)


class GuestDetailsForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phone = forms.IntegerField(min_value=1000000000, max_value=9999999999)
    email = forms.EmailField(required=True)


class NoGuestsRoomForm(forms.Form):
    def __init__(self, count, types, *args, **kwargs):
        super(NoGuestsRoomForm, self).__init__(*args, **kwargs)
        self.fields['no_rooms'] = forms.IntegerField(max_value=count)
        no_guests =  0
        if types == 'Single-AC':
            no_guests = count
        elif types == 'Single-Non-AC':
            no_guests = count
        elif types == 'Double-AC':
            no_guests = count * 2
        elif types == 'Double-Non-AC':
            no_guests = count * 2
        self.fields['no_guests'] = forms.IntegerField(max_value=no_guests)
