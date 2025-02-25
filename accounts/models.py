from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('Customer', 'Customer'),
        # first is actual value, second is human-readable placeholder
        ('Vendor', 'Vendor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField( max_length=50)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=True, blank=True)
    bio = models.CharField(max_length=100)
    image= models.ImageField(upload_to ='uploads/% Y/% m/% d/', blank=True)
    contact_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


# Create your models here.
