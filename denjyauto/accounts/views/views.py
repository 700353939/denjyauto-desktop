from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from denjyauto import settings
from denjyauto.accounts.forms import WorkerUserCreationForm
from denjyauto.accounts.permissions import CustomPermissionRequiredMixin

UserModel = get_user_model()

def login_view(request):
    if request.user.is_authenticated:
        return redirect_after_login(request, request.user)

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect_after_login(request, user)
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def redirect_after_login(request, user):
    base_url = settings.BASE_URL_JS
    if user.groups.filter(name__in=['Admins', 'Workers']).exists() or user.is_superuser:
        return redirect('/common/admin-page')

    elif user.groups.filter(name='Clients').exists():
        return render(request, 'common/home-page.html', {'BASE_URL_JS': base_url})
    else:
        return redirect('/common/home-page')

class RegisterWorker(PermissionRequiredMixin, CreateView):
    model = UserModel
    form_class = WorkerUserCreationForm
    template_name = 'accounts/register-worker.html'
    permission_required = ['accounts.register-worker']
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object

        user.is_staff = True
        user.save()

        group, created = Group.objects.get_or_create(name='Workers')
        user.groups.add(group)

        return response

class WorkerDetails(CustomPermissionRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/details-worker.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['fields'] = [
            (field.verbose_name, getattr(user, field.name))
            for field in user._meta.fields
            if field.name not in ['password', 'id', 'is_superuser', 'is_client']
        ]
        return context