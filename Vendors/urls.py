from django.urls import path
from . import views
from .views import VendorVisitView

urlpatterns = [
    path('', views.home, name='home_page'),
    path('login/', views.vendor_login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profileEdit/', views.profileEdit, name='profileEdit'),
    path('registration/', views.registration, name='registration'),
    path('vendor/<int:vendor_id>/visit/', VendorVisitView.as_view(), name='vendor-visit'),]