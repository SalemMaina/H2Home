from django.contrib.auth.models import User
from .models import CustomerProfile 
from Vendors.models import Vendor
from IOT.models import RandomNumber
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


#class GroupSerializer(serializers.HyperlinkedModelSerializer):
    #class Meta:
        #model = Group
        #fields = ['url', 'name']

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['url', 'user', 'name', 'location' ,'contact_number'] 

class VendorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vendor
        fields = ['url', 'user', 'business_name', 'opening_time', 'closing_time', 'location', 'description', 'price_per_litre', 'email', 'phone_number']
        
