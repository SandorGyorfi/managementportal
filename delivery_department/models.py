from django.db import models
from customer_service.models import Customer
from datetime import date

# Create your models here.
class Delivery(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    STATUS_CHOICES = [
    ('Pending Delivery', 'Pending Delivery'),
    ('Picked Up', 'Picked Up'),
    ('Confirmed Picked Up', 'Confirmed Picked Up'),
    ('Delivered', 'Delivered'),
]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending Delivery')
    delivery_date = models.DateField()

    def __str__(self):
        return f"Delivery for {self.customer.full_name} on {self.delivery_date}"
    

    def is_overdue(self):
        return self.delivery_date < date.today()