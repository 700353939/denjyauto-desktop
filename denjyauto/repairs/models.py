from datetime import date

from django.db import models
from multiselectfield import MultiSelectField

from denjyauto.clients.models import Car


class Repair(models.Model):
    REPAIRS_TYPE = [
        ("OIL FILTER", "Oil Filter"),
        ("FUEL FILTER", "Fuel Filter"),
        ("AIR FILTER", "Air Filter"),
        ("CABIN FILTER", "Cabin Filter"),
        ("DIAGNOSTIC", "Diagnostic"),
        ("OIL CHANGE", "Oil Change"),
        ("TIRE CHANGE", "Tire Change"),
        ("UNDERCARRIAGE REPAIRS", "Undercarriage repairs"),
        ("ENGINE MAINTENANCE", "Engine Maintenance"),
        ("CHECK IN", "Check in"),
    ]
    repair_date = models.DateField(verbose_name= "Date of repair", default=date.today)
    repair_km = models.PositiveIntegerField(blank=True, null=True, verbose_name= "Repair km")
    repairs_type_field = MultiSelectField(choices=REPAIRS_TYPE, verbose_name= "Types repairs")
    repair_price = models.PositiveIntegerField(verbose_name= "Price")
    repair_notes = models.TextField(blank=True, null=True, verbose_name= "Notes")
    car = models.ForeignKey(to=Car, on_delete=models.CASCADE)


class SensitiveRepairInfo(models.Model):
    text = models.TextField(blank=True, null=True, verbose_name= "It's all about...")
    pure_repair_price = models.PositiveIntegerField(verbose_name= "Pure repair price")
    repair = models.OneToOneField(to=Repair, on_delete=models.CASCADE)

