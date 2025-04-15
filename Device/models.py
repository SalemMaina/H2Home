# Device/models.py
from django.db import models
from django.contrib.auth.models import User

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    device_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, blank=True)
    last_active = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.device_id} ({self.user.username if self.user else 'unassigned'})"

class SensorData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.device.device_id}: {self.value} at {self.timestamp}"