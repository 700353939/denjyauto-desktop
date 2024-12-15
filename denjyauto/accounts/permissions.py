from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.http import HttpResponseForbidden


class CustomPermissionRequiredMixin(PermissionRequiredMixin):
    allowed_group = 'Workers'
    permission_required = [
        'clients.car-add',
        'clients.car-details',
        'clients.client-add',
        'clients.client-details',
        'repairs.repair-add'
        'repairs.repair-details'
        'accounts.details-worker'
    ]

    def has_permission(self):
        if super().has_permission():
            return True

        if self.allowed_group:
            return self.request.user.groups.filter(name=self.allowed_group).exists()

        return False

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('home-page')
        return HttpResponseForbidden("You do not have permission to view this page.")
