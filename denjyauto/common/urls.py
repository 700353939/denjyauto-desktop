from django.urls import path

from denjyauto.common.views import home_page, admin_page

urlpatterns = [
    path('', home_page, name='home-page'),
    path('admin-page/', admin_page, name='admin-page')
]