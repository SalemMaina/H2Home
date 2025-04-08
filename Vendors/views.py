from Vendors.forms import VendorForm
from rest_framework.views import APIView

from rest_framework import status
from django.contrib.auth import get_user_model, authenticate, login as auth_login , logout as auth_logout
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Vendor, VendorVisit
from django.contrib.auth.models import User
from .serializers import VendorVisitSerializer
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# Home Page
def home(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(reverse("login"))
    
    try:
        vendor = Vendor.objects.get(user=user)
        
        # Check if the user has a vendor profile
        if not vendor:
            messages.error(request, "You need to complete your vendor profile.")
            return redirect(reverse("registration"))
        
        # Get all visit records for this vendor
        vendor_visits = VendorVisit.objects.filter(vendor=vendor)
        
        # Calculate metrics
        total_visits = vendor_visits.aggregate(
            total=Sum('visit_count')
        )['total'] or 0
        
        today_visits = vendor_visits.filter(
            visit_time__date=timezone.now().date()
        ).aggregate(
            today_total=Sum('visit_count')
        )['today_total'] or 0
        
        # Get the most recent visit records
        recent_visits = vendor_visits.order_by('visit_time')[:10]
        
    except Vendor.DoesNotExist:
        vendor = None
        total_visits = 0
        today_visits = 0
        recent_visits = []
    
    context = {
        'vendor': vendor,
        'total_visits': total_visits,
        'today_visits': today_visits,
        'recent_visits': recent_visits,
    }
    return render(request, 'Vendors/index.html', context)


# Vendor Logout
def vendor_logout(request):
    if request.method == 'POST':
        auth_logout(request)  # Use auth_logout to log out the user
        messages.success(request, "You have been logged out successfully.")
        return redirect(reverse("login"))  # Redirect to login page after logout

    return render(request, 'Vendors/logout.html')  # Render logout confirmation page


# Vendor Login
def vendor_login(request):
    if request.method == 'POST':
        email_or_username = request.POST.get('email').strip()  # Clean input
        password = request.POST.get('password')
        remember_me = request.POST.get('rememberMe')

        # Validation
        if not email_or_username or not password:
            messages.error(request, "Both email and password are required.")
            return render(request, 'Vendors/Login.html')

        User = get_user_model()

        try:
            # Check if input is email or username
            if '@' in email_or_username:
                user = User.objects.get(email__iexact=email_or_username)
            else:
                user = User.objects.get(username__iexact=email_or_username)
            
            # Authenticate
            auth_user = authenticate(request, username=user.username, password=password)
            
            if auth_user is not None:
                auth_login(request, auth_user)
                
                # Handle "Remember Me" functionality
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when browser closes
                
                messages.success(request, f"Welcome back, {auth_user.get_full_name() or auth_user.username}!")
                
                # Redirect to appropriate page
                next_url = request.GET.get('next') or reverse('home_page')
                return redirect(next_url)
                
            else:
                messages.error(request, "Invalid password.")
                
        except User.DoesNotExist:
            messages.error(request, "Account not found. Please check your email.")

    return render(request, 'Vendors/Login.html')


# Vendor Registration
def register(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        # Validation checks
        errors = False
        
        if not email or not password or not confirm_password:
            messages.error(request, "All fields are required")
            errors = True
            
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            errors = True
            
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address")
            errors = True
            
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            errors = True
            
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use")
            errors = True

        if errors:
            return render(request, "Vendors/signup.html", {
                'email': email,
                'password': password,
                'confirm_password': confirm_password
            })

        # Create user and vendor profile
        try:
            username = email.split("@")[0]
            # Ensure username is unique
            counter = 1
            original_username = username
            while User.objects.filter(username=username).exists():
                username = f"{original_username}_{counter}"
                counter += 1
                
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
                        
            messages.success(request, "Registration successful! Please log in.")
            return redirect(reverse("registration"))
            
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
            return render(request, "Vendors/signup.html", {
                'email': email,
                'password': password,
                'confirm_password': confirm_password
            })

    return render(request, "Vendors/signup.html")

# Vendor Profile Page
def profile(request):

    if not request.user.is_authenticated:
        return redirect(reverse("login"))
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        vendor = None
    try:
        vendor_visit = VendorVisit.objects.get(vendor=vendor)
    except VendorVisit.DoesNotExist:
        vendor_visit = None
    # Get all visit records for this vendor
    vendor_visits = VendorVisit.objects.filter(vendor=vendor)
    # Calculate metrics
    total_visits = vendor_visits.aggregate(
        total=Sum('visit_count')
    )['total'] or 0
    today_visits = vendor_visits.filter(
        visit_time__date=timezone.now().date()
    ).aggregate(
        today_total=Sum('visit_count')
    )['today_total'] or 0
    # Get the most recent visit records 
    recent_visits = vendor_visits.order_by('visit_time')[:10]

    context = {
        'user': request.user,
        'vendor': vendor,
        'vendor_visit': vendor_visit,
        'total_visits': total_visits,
        'today_visits': today_visits,
        'recent_visits': recent_visits,
        
    }

    return render(request, 'Vendors/vendorProfile.html', context)

# Edit Vendor Profile
def profileEdit(request):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        vendor = None

    context = {
        'user': request.user,
        'vendor': vendor,
    }
    if request.method == "POST":
        form = VendorForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect(reverse("profile"))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = VendorForm(instance=vendor)
    context['form'] = form
    
    return render(request, 'Vendors/vendorEdit.html' , context)

# Vendor Business Registration
@login_required
def registration(request):
    if request.method == "POST":
        form = VendorForm(request.POST, request.FILES)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user = request.user  # Associate with current user
            vendor.save()
            messages.success(request, "Registration successful!")
            return redirect('home_page')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = VendorForm()
    
    return render(request, 'Vendors/vendorRegistration.html', {'form': form})

class VendorVisitView(APIView):
    """Handle vendor visits"""

    def post(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            visit, created = VendorVisit.objects.get_or_create(vendor=vendor)
            visit.visit_count += 1
            visit.save()
            serializer = VendorVisitSerializer(visit)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, vendor_id):
        """Retrieve the visit count for a vendor"""
        try:
            visit = VendorVisit.objects.get(vendor__id=vendor_id)
            serializer = VendorVisitSerializer(visit)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except VendorVisit.DoesNotExist:
            return Response({"error": "No visit records for this vendor"}, status=status.HTTP_404_NOT_FOUND)
