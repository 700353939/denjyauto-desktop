from django import forms

from denjyauto.clients.models import Client, Car


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude= ['user']


class CarForm(forms.ModelForm):
    BRAND_CHOICES = [
        ("AUDI", "Audi"),
        ("BMW", "BMW"),
        ("MERCEDES", "Mercedes-Benz"),
        ("TOYOTA", "Toyota"),
        ("HONDA", "Honda"),
        ("FORD", "Ford"),
        ("OPEL", "Opel"),
        ("VOLKSWAGEN", "Volkswagen"),
        ("NISSAN", "Nissan"),
        ("HYUNDAI", "Hyundai"),
        ("KIA", "Kia"),
        ("PEUGEOT", "Peugeot"),
        ("RENAULT", "Renault"),
        ("CHEVROLET", "Chevrolet"),
        ("JEEP", "Jeep"),
        ("SUBARU", "Subaru"),
        ("MAZDA", "Mazda"),
        ("LAND_ROVER", "Land Rover"),
        ("VOLVO", "Volvo"),
        ("PORSCHE", "Porsche"),
        ("LEXUS", "Lexus"),
        ("JAGUAR", "Jaguar"),
        ("FIAT", "Fiat"),
        ("ALFA_ROMEO", "Alfa Romeo"),
        ("MITSUBISHI", "Mitsubishi"),
        ("SUZUKI", "Suzuki"),
        ("LADA", "Lada"),
        ("OTHER", "Other")
    ]
    brand = forms.ChoiceField(choices=BRAND_CHOICES, label="Choose a brand",)

    class Meta:
        model = Car
        exclude = ['client']

