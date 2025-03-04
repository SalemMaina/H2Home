# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RandomNumber
import json
from django.shortcuts import render, redirect

@csrf_exempt  # Disable CSRF for simplicity (ensure to use proper security measures in production)
def receive_number(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON payload
            number = data.get("number")
            if number is not None and isinstance(number, int):  # Validate number
                RandomNumber.objects.create(value=number)
                return JsonResponse({"message": "Number received successfully"}, status=200)
            else:
                return JsonResponse({"error": "Invalid data"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

def number_list(request):
    if request.method == "POST":
        number = request.POST.get('number')
        if number.isdigit():  # Ensure only numbers are stored
            RandomNumber.objects.create(value=int(number))
        return redirect('number_list')

    numbers = RandomNumber.objects.all().order_by('-created_at')  # Display numbers in reverse order
    return render(request, 'numbers.html', {'numbers': numbers})