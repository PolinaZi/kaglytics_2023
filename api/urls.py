"""kaglytics URL Configuration

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import SignUpView, competitions_view, EmailVerifyView, SignInView

urlpatterns = [
    path('sign-up', SignUpView.as_view()),
    path('sign-in', SignInView.as_view()),
    path('refresh-token', TokenRefreshView.as_view()),
    path('competitions/active', competitions_view),
    path('email-verify', EmailVerifyView.as_view()),
]
