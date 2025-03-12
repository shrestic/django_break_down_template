from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, logout
from accounts.models import EmailOTP
from accounts.serializers.change_password_serializer import ChangePasswordSerializer
from accounts.serializers.forgot_password_serializer import ForgotPasswordSerializer
from accounts.serializers.login_serializer import LoginSerializer
from accounts.serializers.reset_password_serializer import ResetPasswordSerializer
from accounts.serializers.signup_serializer import SignupSerializer
from accounts.serializers.verify_otp_serializer import VerifyOTPSerializer
from .utils import generate_jwt_for_user, generate_otp, send_otp_email
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail

User = get_user_model()


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()

            code = generate_otp()
            EmailOTP.objects.update_or_create(
                user=user,
                defaults={"code": code, "retries": 0, "last_sent_at": datetime.now()},
            )
            send_otp_email(user, code)

            return Response({"message": "Signup successful. OTP sent to your email."}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    MAX_RETRY = 5

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            code = serializer.validated_data["code"].strip()

            try:
                user = User.objects.get(email=email)
                otp = EmailOTP.objects.get(user=user)

                if otp.is_expired():
                    otp.delete()
                    return Response({"error": "OTP expired"}, status=400)

                if otp.retries >= self.MAX_RETRY:
                    otp.delete()
                    return Response({"error": "Maximum retry limit reached."}, status=400)

                if otp.code != code:
                    otp.retries += 1
                    otp.save()
                    return Response({"error": f"Invalid OTP. Attempt {otp.retries}/{self.MAX_RETRY}"}, status=400)

                user.is_active = True
                user.save()
                otp.delete()

                # 🔥 Gen JWT Token
                tokens = generate_jwt_for_user(user)
                return Response({"message": "Email verified and user activated.", **tokens})

            except (User.DoesNotExist, EmailOTP.DoesNotExist):
                return Response({"error": "Invalid email or OTP"}, status=400)

        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

            # Authenticate password
            user = authenticate(request, username=email, password=password)
            if user is None:
                return Response({"error": "Invalid password."}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.is_active:
                code = generate_otp()
                EmailOTP.objects.update_or_create(
                    user=user,
                    defaults={"code": code, "retries": 0, "last_sent_at": datetime.now()},
                )
                send_otp_email(user, code)
                return Response(
                    {"error": "Account not verified. Email confirmation sent."}, status=status.HTTP_403_FORBIDDEN
                )

            tokens = generate_jwt_for_user(user)

            return Response({"message": "Login successful", **tokens}, status=status.HTTP_200_OK)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ResendOTPView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
                otp, created = EmailOTP.objects.get_or_create(user=user)

                if not created and not otp.resend_allowed():
                    return Response({"error": "Please wait before requesting a new OTP."}, status=429)

                code = generate_otp()
                otp.code = code
                otp.retries = 0
                otp.last_sent_at = datetime.now()
                otp.save()

                send_otp_email(user, code)
                return Response({"message": "New OTP sent successfully."}, status=200)

            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=404)

        return Response(serializer.errors, status=400)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data["old_password"]
            new_password = serializer.validated_data["new_password"]

            if not user.check_password(old_password):
                return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=404)

            # 👉 Generate OTP manually
            code = generate_otp()
            EmailOTP.objects.update_or_create(
                user=user,
                defaults={"code": code, "retries": 0, "last_sent_at": datetime.now()},
            )

            # 👉 Send mail manually
            send_mail(
                subject="Password Reset OTP",
                message=f"Your OTP to reset password is: {code}",
                from_email="no-reply@yourapp.com",
                recipient_list=[email],
            )

            return Response(
                {"message": "OTP sent to your email", "email": email}, status=200  # để frontend giữ email cho bước sau
            )

        return Response({"error": serializer.errors}, status=400)


class VerifyResetOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            otp_code = serializer.validated_data["code"].strip()

            try:
                user = User.objects.get(email=email)
                otp = EmailOTP.objects.get(user=user)
            except (User.DoesNotExist, EmailOTP.DoesNotExist):
                return Response({"error": "Invalid email or OTP"}, status=400)

            if otp.is_expired():
                otp.delete()
                return Response({"error": "OTP expired"}, status=400)

            if otp.code != otp_code:
                otp.retries += 1
                otp.save()
                return Response({"error": f"Invalid OTP. Attempt {otp.retries}"}, status=400)

            # ✅ OTP đúng → xóa luôn OTP
            otp.delete()

            return Response({"message": "OTP verified. You can now reset your password.", "email": email}, status=200)

        return Response({"error": serializer.errors}, status=400)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            new_password = serializer.validated_data["new_password"]
            confirm_password = serializer.validated_data["confirm_password"]

            if new_password != confirm_password:
                return Response({"error": "Passwords do not match"}, status=400)

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)

            user.set_password(new_password)
            user.save()

            return Response({"message": "Password has been reset successfully."}, status=200)

        return Response({"error": serializer.errors}, status=400)
