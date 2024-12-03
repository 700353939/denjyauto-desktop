from django.urls import path

from denjyauto.common.views import home_page, admin_page, search_view, calculate_profit

urlpatterns = [
    path('', home_page, name='home-page'),
    path('admin-page/', admin_page, name='admin-page'),
    path('search/', search_view, name='search'),
    path('calculate-profit/', calculate_profit, name='calculate-profit'),
]