from django.urls import path, include
from rest_framework.routers import DefaultRouter
from denjyauto.reprForClients.views import CarViewSet, RepairViewSet

router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'repairs', RepairViewSet)

urlpatterns = [
    path('', include(router.urls)),
]