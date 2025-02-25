from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import Profile

@receiver(user_signed_up)
def create_profile(user, **kwargs):
    Profile.objects.create(user=user, name=user.username)
