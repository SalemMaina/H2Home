from django.shortcuts import render
from django.contrib.auth.models import User
from .models import CustomerProfile
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .serializers import UserSerializer, ProfileSerializer, VendorSerializer
from Vendors.models import Vendor

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
def perform_create(self, serializer):
        email = serializer.validated_data.get("email", "")
        username = email.split('@')[0]  # Extract first part of email
        serializer.save(username=username)

#class GroupViewSet(viewsets.ModelViewSet):
   
    #queryset = Group.objects.all().order_by('name')
    #serializer_class = GroupSerializer
    #permission_classes = [permissions.IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
def create_profile(request):
     if request.method=='POST':
        serializer=ProfileSerializer(data=request.data)
        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
@api_view(['GET','PUT','DELETE'])
def profile_detail(request,pk):
     try:
        profile=CustomerProfile.objects.get(pk=pk)
     except CustomerProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method=='GET':
            serializer=ProfileSerializer(profile)
            return Response(serializer.data)
        elif request.method=='PUT':
            serializer=ProfileSerializer(profile,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        if request.method=='DELETE':
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
@api_view(['GET','PUT','DELETE'])
def user_detail(request,pk):
     try:
        user=User.objects.get(pk=pk)
     except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method=='GET':
            serializer=UserSerializer(user)
            return Response(serializer.data)
        elif request.method=='PUT':
            serializer=UserSerializer(user,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        if request.method=='DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
class VendorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET','PUT','DELETE'])
def vendor_detail(request,pk):
     try:
        vendor=Vendor.objects.get(pk=pk)
     except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method=='GET':
            serializer=VendorSerializer(user)
            return Response(serializer.data)
        elif request.method=='PUT':
            serializer=VendorSerializer(user,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        if request.method=='DELETE':
            vendor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)