from rest_framework import serializers

from denjyauto.clients.models import Car
from denjyauto.repairs.models import Repair


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'license_plate', 'brand', 'year']


class RepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = ['id', 'repair_km', 'repairs_type_field', 'repair_price','car']
