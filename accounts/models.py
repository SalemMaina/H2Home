from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomerProfile(models.Model):
   
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField( max_length=50)
    contact_number = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=50)


    def __str__(self):
        return str(self.name)


# Create your models here.
