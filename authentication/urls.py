"""
URL configuration for authentication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from accounts import views
from Vendors import urls
from Payments import urls
from Payments.views import SubscriptionPlanViewSet
from Payments import views as Payments

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
<<<<<<< HEAD
router.register(r'groups', views.GroupViewSet)  
=======
#router.register(r'groups', views.GroupViewSet)
>>>>>>> 277beb3 (REST Api updates)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'vendors', views.VendorViewSet)
router.register(r'plans',  Payments.SubscriptionPlanViewSet)

urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('Vendors.urls')),
<<<<<<< HEAD
    path('iot/', include('IOT.urls')),
    path('device/', include('Device.urls')),

=======
    path('payments/', include('Payments.urls')),
>>>>>>> f026378 (Payments module in the backend)
    #path('',include, 'accounts.urls'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))
]
