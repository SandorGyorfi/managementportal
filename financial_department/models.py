from django.db import models
from customer_service.models import Customer


# Create your models here.
class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('Pending Payment', 'Pending Payment'),
        ('Payment Processed', 'Payment Processed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending Payment')
    stripe_bank_details = models.TextField(blank=True, null=True)