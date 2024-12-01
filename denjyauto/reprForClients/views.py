from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from denjyauto.clients.models import Car
from denjyauto.repairs.models import Repair
from denjyauto.reprForClients.serializers import CarSerializer, RepairSerializer


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='Clients').exists():
            return Car.objects.filter(client__username=self.request.user.username)
        return super().get_queryset()


class RepairViewSet(ModelViewSet):
    queryset = Repair.objects.all()
    serializer_class = RepairSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='Clients').exists():
            return Repair.objects.filter(car__client__username=self.request.user.username)
        return super().get_queryset()
