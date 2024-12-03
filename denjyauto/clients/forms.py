from django import forms

from denjyauto.clients.models import Client, Car


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude= ['user']


class CarForm(forms.ModelForm):
    BRAND_CHOICES = [
        ("Audi", "Audi"),
        ("BMW", "BMW"),
        ("Mercedes-Benz", "Mercedes-Benz"),
        ("Toyota", "Toyota"),
        ("Honda", "Honda"),
        ("Ford", "Ford"),
        ("Opel", "Opel"),
        ("Volkswagen", "Volkswagen"),
        ("Nissan", "Nissan"),
        ("Hyundai", "Hyundai"),
        ("Kia", "Kia"),
        ("Peugeot", "Peugeot"),
        ("Renault", "Renault"),
        ("Chevrolet", "Chevrolet"),
        ("Jeep", "Jeep"),
        ("Subaru", "Subaru"),
        ("Mazda", "Mazda"),
        ("Land Rover", "Land Rover"),
        ("Volvo", "Volvo"),
        ("Porsche", "Porsche"),
        ("Lexus", "Lexus"),
        ("Jaguar", "Jaguar"),
        ("Fiat", "Fiat"),
        ("Alfa Romeo", "Alfa Romeo"),
        ("Mitsubishi", "Mitsubishi"),
        ("Suzuki", "Suzuki"),
        ("Lada", "Lada"),
        ("Other", "Other"),
    ]
    brand = forms.ChoiceField(choices=BRAND_CHOICES, label="Choose a brand",)

    class Meta:
        model = Car
        exclude = ['client']

