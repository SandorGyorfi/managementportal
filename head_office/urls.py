from django.urls import path
from . import views

app_name = 'head_office'

urlpatterns = [
    path('head_office/', views.view_head_office, name='head_office'),
]
