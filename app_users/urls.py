from rest_framework.urls import path
from . import views

urlpatterns = [
    path(route="register/", view=views.RegisterView.as_view()),
    path(route="verify/", view=views.VerifyOTPView.as_view()),
]