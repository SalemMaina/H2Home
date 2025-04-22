from django.urls import path
from . import views
from .views import SubscriptionPlanListAPI, SubscriptionPlanViewSet, InitSubscriptionAPI, paystack_webhook


urlpatterns = [
    path('initialize-payment/', views.initialize_payment, name='initialize_payment'),
    path('payment-callback/', views.payment_callback, name='payment_callback'),
    path('initialize-subscription/', views.initialize_subscription, name='initialize_subscription'),
    path('subscription-callback/', views.subscription_callback, name='subscription_callback'),
    path('api/plans/', SubscriptionPlanListAPI.as_view(), name='plan-list'),
    path('api/subscriptions/init/', InitSubscriptionAPI.as_view(), name='init-subscription'),
    path('api/webhook/paystack/', paystack_webhook, name='paystack-webhook'),
]