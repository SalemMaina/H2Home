# device/utils.py
from .models import Device

def check_inactive_devices():
    """Unassign users from inactive devices"""
    inactive_devices = Device.objects.filter(user__isnull=False)
    for device in inactive_devices:
        if device.needs_transfer():
            device.user = None
            device.save()