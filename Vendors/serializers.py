from rest_framework import serializers
from .models import VendorVisit

class VendorVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorVisit
        fields = ["vendor", "visit_count"]
