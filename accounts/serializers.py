from django.contrib.auth.models import Group, User
from .models import CustomerProfile 
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['url', 'user', 'name', 'location' ,'contact_number'] 