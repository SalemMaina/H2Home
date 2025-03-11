from django.shortcuts import render
from django.contrib.auth.models import Group, User
from .models import CustomerProfile
from rest_framework import permissions, viewsets

from .serializers import GroupSerializer, UserSerializer, ProfileSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data.get('email', '')
        username = email.split('@')[0]  # Extract username from email
        validated_data['username'] = username  # Set it as the username

        user = User.objects.create_user(**validated_data)
        return user


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):

    queryset = CustomerProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes =[permissions.IsAuthenticated]