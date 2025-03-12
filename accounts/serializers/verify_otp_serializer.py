# accounts/serializers/verify_otp_serializer.py
from rest_framework import serializers


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
