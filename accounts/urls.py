from django.urls import path
from .views import VendorCustomersView, ChangeCustomerVendorView

urlpatterns = [
    path('vendor/<int:vendor_id>/customers/', VendorCustomersView.as_view(), name='vendor-customers'),
    path('customer/<int:customer_id>/change-vendor/<int:vendor_id>/', ChangeCustomerVendorView.as_view(), name='change-customer-vendor'),
]
