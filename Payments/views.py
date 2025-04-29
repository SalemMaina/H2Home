from django.shortcuts import render
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .models import OneTimePayment, SubscriptionPlan, Subscription, SubscriptionPayment
from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from rest_framework import generics, filters, viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import SubscriptionPlanSerializer, SubscriptionInitSerializer
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.db import transaction
import hmac
import hashlib
import json

# Create your views here.
class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer

class SubscriptionPlanListAPI(generics.ListAPIView):
    """
    List all active subscription plans with filtering capabilities.
    Access: All users (including unauthenticated)
    """
    serializer_class = SubscriptionPlanSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'vendor': ['exact'],  # Filter by vendor ID: /?vendor=1
        'interval': ['exact'],  # Filter by interval: /?interval=monthly
        'amount': ['gte', 'lte'],  # Price range: /?amount__gte=1000&amount__lte=5000
    }
    search_fields = ['name']  # Search: /?search=premium

    def get_queryset(self):
        # Only show active, verified plans
        return SubscriptionPlan.objects.filter(is_active=True)
    
class SubscriptionPlanDetailAPI(generics.RetrieveAPIView):
    """
    Retrieve details of a specific subscription plan.
    Access: All users (including unauthenticated)
    """
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    lookup_field = 'id' # Use 'id' as the lookup field
    lookup_url_kwarg = 'plan_id'
    # This will allow you to access the plan details using /api/plans/<plan_id>/
    




def initialize_payment(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        amount = int(request.POST.get('amount')) * 100  # Convert to kobo

        
        url = 'https://api.paystack.co/transaction/initialize'
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            'email': email,
            'amount': amount,
            'callback_url': request.build_absolute_uri('/payments/payment-callback/'),
        }

        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        

        if response_data['status']:
            return redirect(response_data['data']['authorization_url'])
        else:
            return redirect('payment_failed')
        
        # Handle GET requests (or other methods)
    return render(request, 'paystack/initializepayment.html')
        
def payment_callback(request):
    reference = request.GET.get('reference')
    if not reference:
        return JsonResponse({'status': 'failed', 'reason': 'Missing reference'})
    url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}

    response = requests.get(url, headers=headers)
    response_data = response.json()

    if response_data['status'] and response_data['data']['status'] == 'success':
        data = response_data['data']
        
        # Save to OneTimePayment
        OneTimePayment.objects.create(
            email=data['customer']['email'],
            amount=data['amount'] / 100,  # Convert from kobo
            reference=data['reference'],
            status='success',
            #payment_method=data['channel'],  # e.g., 'card', 'bank'
        )
        
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed'}, status=400)
    
def payment_failed(request):
    return messages.error(request, 'Payment failed. Please try again.')
def payment_success(request):
    return messages.success(request, 'Payment was successful.')

def payment_history(request):
    payments = OneTimePayment.objects.filter(User.id == request.User.id)
    return render(request,  'paystack/payment_history.html', {'payments': payments})


def initialize_subscription(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        plan_code = request.POST.get('plan_code')
        plan_check = requests.get(
              f'https://api.paystack.co/plan/{plan_code}',
              headers={'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
        )
        if not plan_check.json()['status']:
              return JsonResponse({'error': 'Invalid plan code'}, status=400)
        else:
              print("Plan Code Validated:", plan_code)

        url = 'https://api.paystack.co/transaction/initialize'
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            'email': email,
            'plan': plan_code,
            'callback_url': request.build_absolute_uri('payments/subscription-callback/'),
        }

        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        print("Response Data:", response_data)

        # Check if the response is successful
        # and redirect to the authorization URL
        if response_data['status']:
            return redirect(response_data['data']['authorization_url'])
        else:
            return JsonResponse({'error': 'Payment initialization failed'},  status=400)
    else:
        return render (request, 'paystack/initialize_subscription.html')
    
def subscription_callback(request):
        reference = request.GET.get('reference')
        if not reference:
            return JsonResponse({'status': 'failed', 'reason': 'Missing reference'})
        url = f'https://api.paystack.co/transaction/verify/{reference}'
        headers = {'Autthorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
        response = requests.get(url, headers = headers)
        response_data = response.json()
        if response_data['status'] and response_data['data']['status'] == 'success':
            data = response_data['data']

            #Save to Subscription
            Subscription.objects.create(
                email = data['customer']['email'],
                plan_code = data['plan']['plan_code'],
                reference = data['reference'],
                status = 'active',
            )
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed to save to subscription model'}, status = 400)

class InitSubscriptionAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = SubscriptionInitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = serializer.validated_data['plan_id']

        # Prepare Paystack payload
        payload = {
            "email": request.user.email,
            "plan": plan.paystack_plan_code,
            "amount": int (plan.amount * 100),  # Convert to integer
            "metadata": {
                "django_user_id": request.user.id,
                "django_plan_id": plan.id,
                "internal_ref": f"SUB-{request.user.id}-{plan.id}"
            },
            "callback_url":"/subscription/verify/"
        }

        # Call Paystack API
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            "https://api.paystack.co/transaction/initialize",
            headers=headers,
            json=payload
        )
        
        data = response.json()
        if not data.get('status'):
            return Response(
                {"error": "Payment gateway error", "details": data},
                status=502
            )

        # Create pending subscription record
        subscription = Subscription.objects.create(
            customer=request.user,
            plan=plan,
            subscription_code=data['data']['reference'],  # Temporary until confirmed
            status='pending'
        )

        return Response({
            "authorization_url": data['data']['authorization_url'],
            "subscription_id": subscription.id,
            "redirect_url": data['data']['authorization_url'],
        })

@csrf_exempt
@transaction.atomic
def paystack_webhook(request):
    # 1. Verify signature
    secret_key = settings.PAYSTACK_SECRET_KEY.encode()
    signature = request.headers.get('x-paystack-signature', '')
    body = request.body
    
    computed_signature = hmac.new(secret_key, body, hashlib.sha512).hexdigest()
    
    if not hmac.compare_digest(computed_signature, signature):
        return HttpResponse(status=403)

    # 2. Process event
    event = json.loads(body)
    event_type = event['event']
    data = event['data']
    
    try:
        if event_type == 'subscription.create':
            return handle_subscription_create(data)
        elif event_type == 'invoice.payment_success':
            return handle_payment_success(data)
        elif event_type == 'subscription.disable':
            return handle_subscription_disable(data)
        else:
            return HttpResponse(status=200)  # Ignore other events
    except Exception as e:
        # Log full error for debugging
        print(f"Webhook processing failed: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)
    client_ip = request.META.get('REMOTE_ADDR')
    if client_ip not in settings.PAYSTACK_WEBHOOK_IP_WHITELIST:
        return HttpResponse(status=403)
    
def handle_subscription_create(data):
    metadata = data.get('metadata', {})
    
    subscription = Subscription.objects.get_or_create(
        subscription_code=data['subscription_code'],
        defaults={
            'customer_id': metadata.get('django_user_id'),
            'plan_id': metadata.get('django_plan_id'),
            'status': 'active',
            'next_payment_date': data['next_payment_date']
        }
    )
    
    # Record initial payment if present
    if 'authorization' in data:
        SubscriptionPayment.objects.create(
            subscription=subscription,
            amount=data['amount'] / 100,
            reference=data['reference'],
            status='success'
        )
    
    return HttpResponse(status=200)

def handle_payment_success(data):
    subscription = Subscription.objects.get(
        subscription_code=data['subscription']['subscription_code']
    )
    
    SubscriptionPayment.objects.create(
        subscription=subscription,
        amount=data['amount'] / 100,
        reference=data['reference'],
        payment_date=data['paid_at'],
        status='success'
    )
    
    # Update next payment date
    subscription.next_payment_date = data['subscription']['next_payment_date']
    subscription.save()
    
    return HttpResponse(status=200)

def handle_subscription_disable(data):
    Subscription.objects.filter(
        subscription_code=data['subscription_code']
    ).update(
        status='cancelled',
        cancelled_at=data['cancelled_at']
    )
    return HttpResponse(status=200)