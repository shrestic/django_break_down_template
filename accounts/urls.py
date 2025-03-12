from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="api_signup"),  # Đăng ký
    path("signin/", views.LoginView.as_view(), name="api_login"),  # Đăng nhập
    path("signout/", views.LogoutView.as_view(), name="api_logout"),  # Đăng xuất
    path("change-password/", views.ChangePasswordView.as_view(), name="api_change_password"),  # Đổi mật khẩu
    path("forgot-password/", views.ForgotPasswordView.as_view(), name="api_forgot_password"),  # Quên mật khẩu
    path("reset-password/", views.ResetPasswordView.as_view(), name="api_reset_password"),  # Đặt lại mật khẩu
    path("verify-otp/", views.VerifyOTPView.as_view(), name="api_verify_otp"),
    path("verify-reset-otp/", views.VerifyResetOTPView.as_view(), name="api_verify_otp"),
    path("resend-otp/", views.ResendOTPView.as_view(), name="api_resend_otp"),
]
