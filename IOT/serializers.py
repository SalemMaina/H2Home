from rest_framework import serializers
from .models import RandomNumber

class RandomNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = RandomNumber
        fields = ['id', 'number', 'timestamp']
