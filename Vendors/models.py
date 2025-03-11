from django.db import models
from django.contrib.auth.models import User

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to User model
    business_name = models.CharField(max_length=255)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    location = models.CharField(max_length=255)  # Can be changed to GPS coordinates
    description = models.TextField()
    price_per_litre = models.DecimalField(max_digits=6, decimal_places=2)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='vendor_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name
