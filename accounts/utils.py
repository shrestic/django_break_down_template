import random
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(user, code):
    send_mail(
        subject="Your OTP Verification Code",
        message=f"Your OTP code is: {code}",
        from_email="noreply@example.com",
        recipient_list=[user.email],
    )


def generate_jwt_for_user(user):
    """
    Trả về dict gồm access và refresh token cho một user.
    Dùng được trong cả VerifyOTPView / LoginView / ResendTokenView v.v.
    """
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
