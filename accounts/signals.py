from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import CustomerProfile

@receiver(user_signed_up)
def create_profile(user, **kwargs):
    CustomerProfile.objects.create(user=user, name=user.username)
