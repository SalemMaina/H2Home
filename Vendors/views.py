from Vendors.forms import VendorForm
from rest_framework.views import APIView

from rest_framework import status
from django.contrib.auth import get_user_model, authenticate, login as auth_login
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Vendor, VendorVisit
from django.contrib.auth.models import User
from .serializers import VendorVisitSerializer
from django.contrib.auth.decorators import login_required


# Home Page
def home(request):
    user = request.user  # Correct way to get the logged-in user
   
    vendor_visits = VendorVisit.objects.all()  # Fetch all vendor visits
    return render(request, 'Vendors/index.html', {"vendor_visits": vendor_visits, "user": user})

# Vendor Login
def vendor_login(request):
    if request.method == 'POST':
        email_or_username = request.POST.get('email')  # Using 'email' as per your form
        password = request.POST.get('password')

        if not email_or_username or not password:
            messages.error(request, "Both fields are required.")
            return render(request, 'Vendors/Login.html')

        User = get_user_model()

        # If input is an email, get the username
        if '@' in email_or_username:
            try:
                user = User.objects.get(email=email_or_username)
                email_or_username = user.username  # Use username for authentication
            except User.DoesNotExist:
                messages.error(request, "Invalid credentials.")
                return render(request, 'Vendors/Login.html')

        # Authenticate user
        user = authenticate(request, username=email_or_username, password=password)
        if user:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(reverse("home_page"))  # Redirect to profile page
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'Vendors/Login.html')  # Show login form

# Vendor Registration
def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect(reverse("register"))  # Redirect back to registration page

        username = email.split("@")[0]  # Extract username from email

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use")
            return redirect(reverse("register"))

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Registration successful! You can now log in.")
        return redirect(reverse("login"))  # Redirect to login page after successful registration

    return render(request, "Vendors/signup.html")  # Render registration form

# Vendor Profile Page
def profile(request):
    return render(request, 'Vendors/vendorProfile.html')

# Edit Vendor Profile
def profileEdit(request):
    return render(request, 'Vendors/vendorEdit.html')

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
