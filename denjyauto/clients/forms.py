from django import forms

from denjyauto.clients.models import Client, Car


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude= ['user']


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ['client']

