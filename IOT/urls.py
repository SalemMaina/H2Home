from django.urls import path
from .views import receive_number, number_list

urlpatterns = [
    path('api/numbers/', receive_number, name='receive_number'),
    path('display-numbers/', number_list, name='display_numbers'),
]