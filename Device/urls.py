# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.esp_data_receive, name='esp_data_receive'),
    path('commands/<str:device_id>/', views.esp_data_send, name='esp_data_send'),
]