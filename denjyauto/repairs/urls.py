from django.urls import path, include

from denjyauto.repairs.views import RepairAdd, RepairDetails, RepairEdit, repair_delete, SensitiveRepairInfoAdd, \
        SensitiveRepairInfoDetails, SensitiveRepairInfoEdit, sensitiverepairinfo_delete

urlpatterns = [
        path('add/', RepairAdd.as_view(), name='repair-add'),
        path('details/', RepairDetails.as_view(), name='repair-details'),
        path('edit/<int:pk>/', RepairEdit.as_view(), name='repair-edit'),
        path('delete/<int:pk>/', repair_delete, name='repair-delete'),

        path('<int:repair_pk>/', include([
                path('add/', SensitiveRepairInfoAdd.as_view(), name='sensinfo-add'),
                path('details/', SensitiveRepairInfoDetails.as_view(), name='sensinfo-details'),
                path('edit/<int:pk>/', SensitiveRepairInfoEdit.as_view(), name='sensinfo-edit'),
                path('delete/<int:pk>/', sensitiverepairinfo_delete, name='sensinfo-delete'),
        ]))
]
