"""managementportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from customer_service import views as customer_service_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', customer_service_views.operator_login, name='login'),
    path('admin/', admin.site.urls),
    path('customer_service/', include('customer_service.urls')), 
    path('financial_department/', include('financial_department.urls')), 
    path('delivery_department/', include('delivery_department.urls')),  
    path('head_office/', include('head_office.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='operator_login'), name='logout'),
]
