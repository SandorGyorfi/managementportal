from django.urls import path
from . import views

urlpatterns = [
    path('operator_login/', views.operator_login, name='operator_login'),  
    path('add_customer/', views.add_customer, name='add_customer'),
]

