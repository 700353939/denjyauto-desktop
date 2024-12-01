from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView

from denjyauto.accounts.permissions import CustomPermissionRequiredMixin
from denjyauto.clients.forms import ClientForm, CarForm
from denjyauto.clients.models import Client, Car


class ClientCarCombinedCreateView(CustomPermissionRequiredMixin, CreateView):
    template_name = 'clients/clientcar-add.html'

    def get_success_url(self, client_pk):
        return reverse_lazy('client-details', kwargs={'pk': client_pk})

    def get(self, request, *args, **kwargs):
        client_form = ClientForm()
        car_form = CarForm()
        return self.render_to_response({'client_form': client_form, 'car_form': car_form})

    def post(self, request, *args, **kwargs):
        client_form = ClientForm(request.POST)
        car_form = CarForm(request.POST)

        if client_form.is_valid() and car_form.is_valid():
            client = client_form.save()

            car = car_form.save(commit=False)
            car.client = client
            car.save()

            return redirect(self.get_success_url(client.pk))
        else:
            return self.render_to_response({'client_form': client_form, 'car_form': car_form})


class ClientDetails(CustomPermissionRequiredMixin, DetailView):
    model = Client
    template_name = 'clients/client-details.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.get_object()
        context['fields'] = [(field.verbose_name, getattr(client, field.name)) for field in client._meta.fields]
        return context


class ClientEdit(PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client-edit.html'
    permission_required = ['clients.client-edit']

    def get_success_url(self):
        return reverse_lazy('client-details', kwargs={'pk': self.object.pk})


def client_delete(request, pk):
    if not request.user.has_perm('clients.client-delete'):
        raise PermissionDenied
    client = Client.objects.get(pk=pk)
    client.delete()
    return redirect('admin-page')


class CarAdd(CustomPermissionRequiredMixin, View):
    template_name = 'clients/car-add.html'

    def get(self, request, client_pk, *args, **kwargs):
        client = get_object_or_404(Client, pk=client_pk)
        form = CarForm()
        return render(request, 'clients/car-add.html', {'form': form, 'client': client})

    def post(self, request, client_pk, *args, **kwargs):
        client = get_object_or_404(Client, pk=client_pk)
        form = CarForm(request.POST)

        if form.is_valid():
            car = form.save(commit=False)
            car.client = client
            car.save()
            return redirect('client-details', pk=client.pk)

        return render(request, 'clients/car-add.html', {'form': form, 'client': client})


class CarDetails(CustomPermissionRequiredMixin, DetailView):
    model = Car
    template_name = 'clients/car-details.html'
    context_object_name = 'car'

    def get_object(self, queryset=None):
        client_pk = self.kwargs.get('client_pk')
        car_pk = self.kwargs.get('pk')

        client = get_object_or_404(Client, pk=client_pk)
        car = get_object_or_404(Car, pk=car_pk, client=client)
        return car

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()
        context['fields'] = [(field.verbose_name, getattr(car, field.name)) for field in car._meta.fields]
        context['client_name'] = car.client.name
        context['client_pk'] = car.client.pk
        return context


class CarEdit(PermissionRequiredMixin, UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'clients/car-edit.html'
    permission_required = ['clients.car-edit']

    def get_success_url(self):
        return reverse_lazy('car-details', kwargs={
                'client_pk': self.object.client.pk,
                'pk': self.object.pk
            }
        )


def car_delete(request, client_pk, pk):
    if not request.user.has_perm('clients.car-delete'):
        raise PermissionDenied
    client = get_object_or_404(Client, pk=client_pk)
    car = get_object_or_404(Car, pk=pk, client=client)
    car.delete()
    return redirect('client-details', pk=client_pk)
