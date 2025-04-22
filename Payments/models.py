from django.db import models
from django.contrib.auth.models import User
from Vendors.models import Vendor

class SubscriptionPlan(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans')
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interval = models.CharField(max_length=20, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'), 
        ('yearly', 'Yearly')
    ])
    is_active = models.BooleanField(default=False)  # ← New: Only show active plans to customers
    paystack_plan_code = models.CharField(  # ← New: Stores Paystack's ID after manual creation
        max_length=50,
        blank=True,
        help_text="Set automatically after creating plan in Paystack dashboard"
    )
    
    def __str__(self):
        return f"{self.name} (₦{self.amount})"
    class Meta:
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'

class Subscription(models.Model):
    customer = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    email= models.EmailField()
    subscription_code = models.CharField(max_length=100)  # Paystack's subscription ID
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled')
    ], default='active')
    start_date = models.DateTimeField(auto_now_add=True)
    next_payment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer.email} - {self.plan.name} ({self.status})"
    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'




class SubscriptionPayment(models.Model):
    #subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='payments')
    email= models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('success', 'Success'),
        ('failed', 'Failed')
    ])
    def __str__(self):
        return f"{self.subscription.customer.email} - {self.amount} ({self.status})"
    class Meta:
        verbose_name = 'Subscription Payment'
        verbose_name_plural = 'Subscription Payments'
        #class Meta:
            #unique_together = ('subscription', 'reference')
        # Ensure a payment is unique to a subscription

class OneTimePayment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_payments')
    email= models.EmailField()
    vendor = models.ForeignKey('Vendors.Vendor', on_delete=models.CASCADE, related_name='vendor_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
   
    def __str__(self):
        return f"{self.customer.email} - {self.amount} ({self.status})"
    class Meta:
        verbose_name = 'One-Time Payment'
        verbose_name_plural = 'One-Time Payments'


