# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RandomNumber
import json
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RandomNumberSerializer


@api_view(['POST'])
def receive_random_number(request):
    serializer = RandomNumberSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # Save the number in the database
        return Response({"message": "Number received", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_random_numbers(request):
    numbers = RandomNumber.objects.all().order_by('-timestamp')
    serializer = RandomNumberSerializer(numbers, many=True)
    return Response(serializer.data)