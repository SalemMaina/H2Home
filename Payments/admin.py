from django.contrib import admin
from .models import SubscriptionPlan, OneTimePayment, Subscription, SubscriptionPayment

# Register your models here.
admin.site.register(SubscriptionPlan)
admin.site.register(OneTimePayment)
admin.site.register(Subscription)
admin.site.register(SubscriptionPayment)

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'amount', 'is_active', 'paystack_plan_code')
    list_filter = ('is_active', 'interval')
    readonly_fields = ('paystack_plan_code',)  # Prevent manual edits
    actions = ['mark_as_verified']

    def mark_as_verified(self, request, queryset):
        """Admin action to manually verify plans"""
        queryset.update(is_active=True)
    mark_as_verified.short_description = "Mark selected plans as verified"

class SubscriptionPlanAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['is_active', 'paystack_plan_code']
        return super().get_readonly_fields(request, obj)