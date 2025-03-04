from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_page'),

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profileEdit/', views.profileEdit, name='profileEdit'),
    path('registration/', views.registration, name='registration'),
]