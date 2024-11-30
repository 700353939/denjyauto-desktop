from django.urls import path

from denjyauto.accounts.views import login_view, RegisterWorker

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', RegisterWorker.as_view(), name='register-worker')
]