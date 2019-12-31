
"""quora URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth.decorators import login_required

from .views import CreateUser, Profile, AnonProfile, PasswordChange, UpdateProfile

urlpatterns = [
    path('signup/', CreateUser.as_view(), name='signup'),
    path('profile/update/', login_required(UpdateProfile.as_view()), name='profile-update'),
    path('profile/', login_required(Profile.as_view()), name='profile'),
    path('profile/user/<username>/', AnonProfile.as_view(), name='anon-profile'),
    path('password_change/', PasswordChange.as_view(), name='password-change')
]
