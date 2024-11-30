"""
URL configuration for denjyauto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from tempfile import template

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [

    path('', TemplateView.as_view(template_name="common/home-page.html")),
    path('admin/', admin.site.urls),
    path('common/', include('denjyauto.common.urls')),
    path('accounts/', include('denjyauto.accounts.urls')),
    path('clients/', include('denjyauto.clients.urls')),
    path('<int:client_pk>/<int:car_pk>/repairs/', include('denjyauto.repairs.urls')),
    path('api/', include('denjyauto.reprForClients.urls')),
]
