from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import CustomUser, EmailConfirmationCode
from .serializers import RegisterSerializer, VerifyOTPSerializer


class RegisterView(APIView):
    def patch(self, request):
        serializer = RegisterSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={
                "message":"Ro'yxatdan muvaffaqiyatli o'tdingiz!",
                "data":serializer.data
            },
            status=status.HTTP_200_OK
        )


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        last_send_code = serializer.validated_data["last_send_code"]
        user.is_verified = True
        user.save()
        last_send_code.is_used = True
        last_send_code.save()
            

        return Response(
            data={
                "message":"Email muvaffaqiyatli tasdiqlandi!"
            },
            status=status.HTTP_200_OK
            )