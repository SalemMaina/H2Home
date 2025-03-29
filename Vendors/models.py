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
    website = models.URLField(blank=True, null=True ) 
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='vendor_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name

class VendorVisit(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="visits")
    visit_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.vendor.business_name} - {self.visit_count} visits"