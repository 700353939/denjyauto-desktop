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
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name= "Phone number"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name= "Email"
    )
    points = models.PositiveIntegerField(
        default=0,
        verbose_name="Points"
    )
    user = models.OneToOneField(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


class Car(models.Model):
    license_plate = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="License plate"
    )
    vin = models.CharField(
        max_length=17,
        verbose_name= "VIN"
    )
    brand = models.CharField(
        max_length=50,
        verbose_name="Brand",
        blank=True, null=True
    )
    year = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name= "Year"
    )
    first_visit = models.DateField(
        auto_now_add=True,
        verbose_name= "First visit"
    )
    car_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name= "Notes about car"
    )
    client = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        self.license_plate = self.license_plate.upper()
        self.vin = self.vin.upper()
        super().save(*args, **kwargs)

