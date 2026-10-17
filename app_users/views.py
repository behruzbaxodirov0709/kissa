from django.shortcuts import render
from rest_framework.response import Response
from django.core.mail import send_mail  
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, EmailConfirmationCode
from . import serializers
import random


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class RegisterView(APIView):
    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={
                "message":"Ro'yxatdan muvaffaqiyatli o'tdingiz!",
                "data":serializer.data
            },
            status=status.HTTP_200_OK
        )


class LoginView(APIView):
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        tokens = get_tokens_for_user(user=user)


        return Response(
            data={
                "message":"Login muvaffaqiyatli amalga oshirildi",
                "tokens":tokens
            },
            status=status.HTTP_200_OK
        )
    

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = serializers.VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        last_send_code = serializer.validated_data["last_send_code"]
        user.is_verified = True
        user.save()
        last_send_code.is_used = True
        last_send_code.save()

        tokens = get_tokens_for_user(user=user)

        return Response(
            data={
                "message":"Email muvaffaqiyatli tasdiqlandi!",
                "tokens":tokens
            },
            status=status.HTTP_200_OK
            )


class ResendOTPView(APIView):
    def post(self, request):
        serializer = serializers.ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = CustomUser.objects.get(email=email)
        email_object = EmailConfirmationCode.objects.filter(user=user, is_used=False).last()
        if email_object:    
            email_object.is_used = True
            email_object.save()
        code =str(random.randint(100000, 999999))

        EmailConfirmationCode.objects.create(user=user, code=code)

        send_mail(
            subject="Kissa — Yangi tasdiqlash kodi",
            message=f"Sizning yangi tasdiqlash kodingiz: {code}",
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'bekzodovich0709@gmail.com'),
            recipient_list=[user.email],
            fail_silently=False
        )

        return Response(
            data={
                "message":"Yangi tasdiqlash kodi emailga yuborildi."
            },
            status=status.HTTP_200_OK
        )