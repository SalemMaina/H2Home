from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'Vendors/index.html')

def login(request):
    return render(request, 'Vendors/login.html')

def register(request): 
    return render(request, 'Vendors/signin.html')

def profile(request):
    return render(request, 'Vendors/vendorProfile.html')

def profileEdit(request):
    return render(request, 'Vendors/vendorEdit.html')

def registration(request):
    return render(request, 'Vendors/vendorRegistration.html')

