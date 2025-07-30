from django.urls import path
from .views import RegisterView, OTPVerifyView, LoginView


urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('verify-otp/', OTPVerifyView.as_view(), name="email-verify"),
]