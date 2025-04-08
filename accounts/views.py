from django.shortcuts import render
from django.contrib.auth.models import Group, User

from Vendors.models import Vendor
from .models import CustomerProfile
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import status


from rest_framework.views import APIView
from .serializers import GroupSerializer, UserSerializer, ProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):

    queryset = CustomerProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes =[permissions.IsAuthenticated]

class VendorCustomersView(APIView):
    """Retrieve all customers of a specific vendor"""

    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            customers = CustomerProfile.objects.filter(vendor=vendor)
            serializer = ProfileSerializer(customers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        
class ChangeCustomerVendorView(APIView):
    """Update the vendor assigned to a customer"""

    def put(self, request, customer_id, vendor_id):
        try:
            customer = CustomerProfile.objects.get(id=customer_id)
            new_vendor = Vendor.objects.get(id=vendor_id)

            customer.vendor = new_vendor
            customer.save()

            serializer = ProfileSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except CustomerProfile.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
