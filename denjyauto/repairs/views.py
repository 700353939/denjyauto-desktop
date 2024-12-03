from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from denjyauto.accounts.permissions import CustomPermissionRequiredMixin
from denjyauto.clients.models import Client, Car
from denjyauto.repairs.forms import RepairForm, SensitiveRepairInfoForm
from denjyauto.repairs.models import Repair, SensitiveRepairInfo


class RepairAdd(CustomPermissionRequiredMixin, View):
    template_name = 'repairs/repair-add.html'

    def get(self, request, client_pk, car_pk, *args, **kwargs):
        client = get_object_or_404(Client, pk=client_pk)
        car = get_object_or_404(Car, pk=car_pk)
        form = RepairForm()
        return render(
            request,
            'repairs/repair-add.html',
            {'form': form, 'client': client, 'car': car}
        )

    def post(self, request, client_pk, car_pk, *args, **kwargs):
        client = get_object_or_404(Client, pk=client_pk)
        car = get_object_or_404(Car, pk=car_pk)
        form = RepairForm(request.POST)
        if form.is_valid():
            repair = form.save(commit=False)
            repair.car = car
            repair.save()
            return redirect('repair-details', client_pk=client.pk, car_pk=car.pk)

        return render(
            request,
            'repairs/repair-add.html',
            {'form': form, 'client': client, 'car': car}
            )


class RepairDetails(CustomPermissionRequiredMixin, View):
    template_name = 'repairs/repair-details.html'

    def get(self, request, client_pk, car_pk, *args, **kwargs):
        client = get_object_or_404(Client, pk=client_pk)
        car = get_object_or_404(Car, pk=car_pk, client=client)
        repairs = Repair.objects.filter(car=car)

        repair_fields = []
        for repair in repairs:
            fields = []
            for field in repair._meta.fields:
                if field.name not in ['car', 'id']:
                    value = getattr(repair, field.name)
                    fields.append({
                        'key': field.verbose_name,
                        'value': value,
                    })

            has_sensinfo = SensitiveRepairInfo.objects.filter(repair=repair).exists()

            repair_fields.append({
                'repair': repair,
                'fields': fields,
                'has_sensinfo': has_sensinfo,
            })

        context = {
            'repairs': repair_fields,
            'client': client,
            'car': car,
        }
        return render(request, self.template_name, context)


class RepairEdit(PermissionRequiredMixin, UpdateView):
    model = Repair
    form_class = RepairForm
    template_name = 'repairs/repair-edit.html'
    permission_required = ['repairs.repair-edit']

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('repair-details', kwargs={
                'client_pk': self.object.car.client.pk,
                'car_pk': self.object.car.pk,
            }
        )


def repair_delete(request, client_pk, car_pk, pk):
    if not request.user.has_perm('clients.car-delete'):
        raise PermissionDenied

    client = get_object_or_404(Client, pk=client_pk)
    car = get_object_or_404(Car, pk=car_pk, client=client)
    repair = get_object_or_404(Repair, pk=pk, car=car)
    repair.delete()
    return redirect('repair-details', client_pk=client.pk, car_pk=car.pk)


class SensitiveRepairInfoAdd(PermissionRequiredMixin, View):
    template_name = 'repairs/sensinfo-add.html'
    permission_required = ['repairs.sensinfo-add']

    def get(self, request, client_pk, car_pk, repair_pk, *args, **kwargs):
        client = get_object_or_404(Client, pk=client_pk)
        car = get_object_or_404(Car, pk=car_pk)
        repair = get_object_or_404(Repair, pk=repair_pk)
        form = SensitiveRepairInfoForm()
        return render(
            request,
            'repairs/sensinfo-add.html',
            {'form': form, 'client': client, 'car': car, 'repair': repair}
        )

    def post(self, request, client_pk, car_pk, repair_pk, *args, **kwargs):
        client = get_object_or_404(Client, pk=client_pk)
        car = get_object_or_404(Car, pk=car_pk)
        repair = get_object_or_404(Repair, pk=repair_pk)
        form = SensitiveRepairInfoForm(request.POST)
        if form.is_valid():
            sensinfo = form.save(commit=False)
            sensinfo.repair = repair
            sensinfo.save()
            return redirect('sensinfo-details', client_pk=client.pk, car_pk=car.pk, repair_pk=repair.pk)

        return render(
            request,
            'repairs/sensinfo-add.html',
            {'form': form, 'client': client, 'car': car, 'repair': repair}
            )


class SensitiveRepairInfoDetails(PermissionRequiredMixin, View):
    template_name = 'repairs/sensinfo-details.html'
    permission_required = ['repairs.sensinfo-details']

    def get(self, request, client_pk, car_pk, repair_pk, *args, **kwargs):
        client = get_object_or_404(Client, pk=client_pk)
        car = get_object_or_404(Car, pk=car_pk, client=client)
        repair = get_object_or_404(Repair, pk=repair_pk)

        sensinfo_queryset = SensitiveRepairInfo.objects.filter(repair=repair)

        if sensinfo_queryset.exists():
            sensinfo = sensinfo_queryset.first()
            sensinfo_fields = [
                (field.verbose_name, getattr(sensinfo, field.name))
                for field in sensinfo._meta.fields if field.name != 'repair'
            ]
        else:
            sensinfo = None
            sensinfo_fields = []

        context = {
            'sensinfo': sensinfo,
            'sensinfo_fields': sensinfo_fields,
            'client': client,
            'car': car,
            'repair': repair,
        }
        return render(request, self.template_name, context)

class SensitiveRepairInfoEdit(PermissionRequiredMixin, UpdateView):
    model = SensitiveRepairInfo
    form_class = SensitiveRepairInfoForm
    template_name = 'repairs/sensinfo-edit.html'
    permission_required = ['repairs.sensinfo-edit']

    def get_success_url(self):
        return reverse_lazy('sensinfo-details', kwargs={
                'client_pk': self.object.repair.car.client.pk,
                'car_pk': self.object.repair.car.pk,
                'repair_pk': self.object.repair.pk,
            }
        )


def sensitiverepairinfo_delete(request, client_pk, car_pk, repair_pk, pk):
    if not request.user.has_perm('clients.sensinfo-delete'):
        raise PermissionDenied

    client = get_object_or_404(Client, pk=client_pk)
    car = get_object_or_404(Car, pk=car_pk, client=client)
    repair = get_object_or_404(Repair, pk=repair_pk, car=car)
    sensinfo = get_object_or_404(SensitiveRepairInfo, pk=pk, repair=repair)
    sensinfo.delete()
    return redirect('repair-details', client_pk=client_pk, car_pk=car_pk)