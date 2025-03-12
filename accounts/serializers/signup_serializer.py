import random
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.mail import send_mail

from accounts.models import EmailOTP

User = get_user_model()


def generate_otp():
    return str(random.randint(100000, 999999))


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists.")
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")
        return email

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password1"],
            is_active=False,  # 🚫 Đừng kích hoạt ngay
        )

        code = generate_otp()
        EmailOTP.objects.create(user=user, code=code)

        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP code is: {code}",
            from_email="noreply@yourdomain.com",
            recipient_list=[user.email],
        )
        return user
