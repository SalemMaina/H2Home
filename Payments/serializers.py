from rest_framework import serializers
from .models import SubscriptionPlan, Subscription

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.get_full_name', read_only=True)
    
    class Meta:
        model = SubscriptionPlan
        fields = [
            'id',
            'name',
            'amount',
            'interval',
            'vendor_name',
            'paystack_plan_code'  # Needed for subscription initialization
        ]
        read_only_fields = fields  # All fields are read-only for customers

class SubscriptionInitSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()
    
    def validate_plan_id(self, value):
        """Verify plan exists and is active"""
        plan = SubscriptionPlan.objects.filter(id=value, is_active=True).first()
        if not plan:
            raise serializers.ValidationError("Invalid or inactive plan")
        return plan