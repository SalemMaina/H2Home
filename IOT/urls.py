from django.urls import path
from .views import receive_random_number, get_random_numbers
urlpatterns = [
    path('api/receive_number/', receive_random_number, name='receive_number'),
    path('api/get_numbers/', get_random_numbers, name='get_numbers'),
]