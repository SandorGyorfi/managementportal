from django.urls import path
from . import views

app_name = 'financial_department'  

urlpatterns = [
    path('payments/', views.view_payments, name='view_payments'),
    path('process_payment/<int:payment_id>/', views.process_payment, name='process_payment'),  
]
