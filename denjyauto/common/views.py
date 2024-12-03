from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from denjyauto.common.forms import DateRangeForm
from denjyauto.clients.forms import ClientForm
from denjyauto.clients.models import Client, Car
from denjyauto.repairs.models import Repair, SensitiveRepairInfo


def home_page(request):
    return render(request, template_name='common/home-page.html')

@login_required
def admin_page(request):
    if not request.user.is_staff:
        return home_page(request)

    all_clients = Client.objects.all()
    clients_form = ClientForm()

    clients_per_page = 10
    paginator = Paginator(all_clients, clients_per_page)
    page = request.GET.get('page')

    try:
        all_clients = paginator.page(page)
    except PageNotAnInteger:
        all_clients = paginator.page(1)
    except EmptyPage:
        all_clients = paginator.page(paginator.num_pages)

    context = {
        'all_clients': all_clients,
        'clients_form': clients_form,
    }
    return render(request, 'common/admin-page.html', context=context)

def search_view(request):
    query = request.GET.get('query', '')
    results = []

    if query:
        clients = Client.objects.filter(name__icontains=query)
        cars = Car.objects.filter(license_plate__icontains=query)

        for client in clients:
            results.append({
                'type': 'client',
                'id': client.id,
                'client_name': client.name,
            })

        for car in cars:
            results.append({
                'type': 'car',
                'id': car.id,
                'client_id': car.client.id,
                'license_plate': car.license_plate,
            })

    return render(request, 'common/search.html', {'results': results})


def calculate_profit(request):
    profit = None
    repairs_list = None

    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']

            repairs = Repair.objects.filter(repair_date__range=(from_date, to_date))

            repairs_list = []
            profit = 0
            for repair in repairs:
                try:
                    sensitive_info = SensitiveRepairInfo.objects.get(repair=repair)
                    profit += repair.repair_price - sensitive_info.pure_repair_price

                    repairs_list.append(
                    {
                        'date': repairs.repair_date,
                        'client_price': repair.repair_price,
                        'pure_price': sensitive_info.pure_repair_price,
                        'base_profit': repair.repair_price - sensitive_info.pure_repair_price
                        }
                    )

                except SensitiveRepairInfo.DoesNotExist:

                    continue

    else:
        form = DateRangeForm()

    return render(
        request,
        'common/calculate_profit.html',
        {'form': form, 'profit': profit, 'repairs_list': repairs_list}
    )

