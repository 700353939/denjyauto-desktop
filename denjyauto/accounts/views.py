from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView

from denjyauto.accounts.forms import WorkerUserCreationForm

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
    if user.groups.filter(name__in=['Admins', 'Workers']).exists():
        return redirect('/common/admin-page')

    elif user.groups.filter(name='Clients').exists():
        return redirect('api-root')
    else:
        return redirect('/common/')

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
