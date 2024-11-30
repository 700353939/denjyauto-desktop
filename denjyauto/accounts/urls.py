from django.contrib.auth.views import LogoutView
from django.urls import path


from denjyauto.accounts.views import login_view, RegisterWorker

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterWorker.as_view(), name='register-worker')
]