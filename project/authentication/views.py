import pyotp
from rest_framework import generics
from rest_framework.response import Response
from .models import User
from .serializers import OTPVerificationSerializer, RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from .renderers import UserRenderer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)
    def perform_create(self, serializer):
        user = serializer.save()
        user.otp_secret = pyotp.random_base32()
        user.is_verified = False
        user.save()
        totp = pyotp.TOTP(user.otp_secret, interval=300)
        otp = totp.now()
        Util.send_sms({"phone": user.phone, "otp": otp})
        return Response({'detail': 'OTP sent to phone'})

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        phone = request.data.get('phone')
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        totp = pyotp.TOTP(user.otp_secret, interval=300)
        otp = totp.now()
        Util.send_sms({"phone": user.phone, "otp": otp})
        return Response({'detail': 'OTP sent to phone'})

class OTPVerifyView(generics.GenericAPIView):
    serializer_class = OTPVerificationSerializer

    def post(self, request):
        phone = request.data.get('phone')
        otp = request.data.get('otp')
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        # if not user.otp_secret:
        #     return Response({'error': 'Registration incomplete'}, status=400)

        totp = pyotp.TOTP(user.otp_secret, interval=300)
        if totp.verify(otp):
            user.is_verified = True
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'phone': user.phone
            })
        return Response({'error': 'Invalid OTP'}, status=400)
