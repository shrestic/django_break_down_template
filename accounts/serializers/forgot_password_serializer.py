# accounts/serializers/forgot_password_serializer.py
from rest_framework import serializers


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
