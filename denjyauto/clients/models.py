from django.core.validators import MinLengthValidator
from django.db import models


class Client(models.Model):
    name = models.CharField(
        validators=[MinLengthValidator(3)],
        max_length=30,
        unique=True,
        verbose_name= "Client name"
    )
    username = models.CharField(
        validators=[MinLengthValidator(3)],
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Client username"
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name= "Phone number")
    email = models.EmailField(blank=True, null=True, verbose_name= "Email")
    points = models.PositiveIntegerField(default=0, verbose_name="Points")


class Car(models.Model):
    BRANDS = [
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
    license_plate = models.CharField(max_length=10, unique=True, verbose_name="License plate")
    vin = models.CharField(max_length=17, verbose_name= "VIN")
    brand = models.CharField(choices=BRANDS, verbose_name= "Brand")
    year = models.PositiveIntegerField(blank=True, null=True, verbose_name= "Year")
    first_visit = models.DateField(auto_now_add=True, verbose_name= "First visit")
    car_notes = models.TextField(blank=True, null=True, verbose_name= "Notes about car")
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.license_plate = self.license_plate.upper()
        self.vin = self.vin.upper()
        super().save(*args, **kwargs)

