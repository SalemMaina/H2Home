from django.db import models
from django.contrib.auth.models import User
from Vendors.models import Vendor
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    contact_number = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=50)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True, related_name="customers")

    def __str__(self):
        return str(self.name)
