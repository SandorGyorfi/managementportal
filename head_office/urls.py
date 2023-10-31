from django.urls import path
from . import views

app_name = 'head_office'

urlpatterns = [
    path('head_office/', views.view_head_office, name='view_head_office'),
    path('delete_payment/<int:payment_id>/', views.delete_payment, name='delete_payment'),
    path('delete_delivery/<int:delivery_id>/', views.delete_delivery, name='delete_delivery'),
]
