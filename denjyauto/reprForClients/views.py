from denjyauto.clients.models import Car
from denjyauto.repairs.models import Repair
from denjyauto.reprForClients.serializers import CarSerializer, RepairSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet


class CarViewSet(ReadOnlyModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name='Clients').exists():
            return Car.objects.filter(client__pk=self.request.user.client.pk)
        return Car.objects.none()


class RepairViewSet(ReadOnlyModelViewSet):
    queryset = Repair.objects.all()
    serializer_class = RepairSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name='Clients').exists():
            car_ids = self.request.user.client.car_set.values_list('pk', flat=True)
            return Repair.objects.filter(car__pk__in=car_ids)
        return Repair.objects.none()

