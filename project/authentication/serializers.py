from rest_framework import serializers
from .models import User
import pyotp




class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone']

    def validate(self, attrs):
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError('The Username should not contain special characters and spaces')
        return attrs

    def create(self, validated_data):
        
        user = User.objects.create_user(**validated_data)
        user.otp_secret = pyotp.random_base32()
        user.save()
        return user


class OTPVerificationSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp = serializers.CharField(max_length=6)


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()