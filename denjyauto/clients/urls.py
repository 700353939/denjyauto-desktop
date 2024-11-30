from django.urls import path, include
from denjyauto.clients.views import ClientCarCombinedCreateView, ClientEdit, ClientDetails, client_delete, CarAdd, \
    CarDetails, CarEdit, car_delete

urlpatterns = [
    path('add/', ClientCarCombinedCreateView.as_view(), name='clientcar-add'),
    path('edit/<int:pk>', ClientEdit.as_view(), name='client-edit'),
    path('details/<int:pk>', ClientDetails.as_view(), name='client-details'),
    path('delete/<int:pk>', client_delete, name='client-delete'),

    path('<int:client_pk>/', include([
        path('add-car/', CarAdd.as_view(), name='car-add'),
        path('car-details/<int:pk>', CarDetails.as_view(), name='car-details'),
        path('car-edit/<int:pk>', CarEdit.as_view(), name='car-edit'),
        path('car-delete/<int:pk>', car_delete, name='car-delete'),
    ]))
]
# path('api/') # GO REST reprForClients