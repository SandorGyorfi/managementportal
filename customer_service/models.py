from django.db import models

# Create your models here.
class Customer(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address_uk = models.TextField()
    delivery_address = models.TextField(blank=True, null=True)
    
    BED_TYPE_CHOICES = [
        ('new', 'New (£1200)'),
        ('used', 'Used (£650)'),
    ]
    bed_type = models.CharField(max_length=5, choices=BED_TYPE_CHOICES)
    requested_delivery_date = models.DateField()

    def get_bed_price(self):
        """Retrieve the price of the bed based on its type."""
        return 1200 if self.bed_type == "new" else 650

    def __str__(self):
        return self.full_name
