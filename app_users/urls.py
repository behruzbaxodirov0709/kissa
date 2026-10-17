from rest_framework.urls import path
from . import views

urlpatterns = [
    path(route="register/", view=views.RegisterView.as_view()),
    path(route="login/", view=views.LoginView.as_view()),
    path(route="verify/", view=views.VerifyOTPView.as_view()),
    path(route="resend-otp/", view=views.ResendOTPView.as_view())
]