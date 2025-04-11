from django.contrib.auth.views import LogoutView
from django.urls import path


from denjyauto.accounts.views.views import login_view, RegisterWorker, WorkerDetails

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterWorker.as_view(), name='register-worker'),
    path('worker-details/<int:pk>/', WorkerDetails.as_view(), name='details-worker')
]