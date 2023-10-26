from django.urls import path
from . import views

app_name = 'delivery_department'

urlpatterns = [
    path('deliveries/', views.view_deliveries, name='view_deliveries'),
    path('pickup/<int:delivery_id>/', views.update_delivery, name='pickup_delivery'),
]
