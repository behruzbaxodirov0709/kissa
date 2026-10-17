from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from django.core.mail import send_mail  
from django.conf import settings
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, EmailConfirmationCode, Account, Category, Transaction
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






class AccountListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        serializer = serializers.AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = serializers.AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        account = get_object_or_404(Account, pk=pk, user=request.user)
        serializer = serializers.AccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        account = get_object_or_404(Account, pk=pk, user=request.user)
        serializer = serializers.AccountSerializer(account, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        account = get_object_or_404(Account, pk=pk, user=request.user)
        account.delete()
        return Response({"message": "Hisob o'chirildi"}, status=status.HTTP_204_NO_CONTENT)



class CategoryListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        categories = Category.objects.filter(user=request.user)
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = serializers.CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk, user=request.user)
        serializer = serializers.CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk, user=request.user)
        serializer = serializers.CategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk, user=request.user)
        category.delete()
        return Response({"message": "Kategoriya o'chirildi"}, status=status.HTTP_204_NO_CONTENT)



class TransactionListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
        serializer = serializers.TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = serializers.TransactionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        transaction = serializer.save(user=request.user)
        account = transaction.account


        if transaction.type == 'income':
            account.balance += transaction.amount
        elif transaction.type == 'expense':
            account.balance -= transaction.amount
        account.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransactionDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        serializer = serializers.TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        account = transaction.account


        if transaction.type == 'income':
            account.balance -= transaction.amount
        elif transaction.type == 'expense':
            account.balance += transaction.amount
        account.save()

        transaction.delete()
        return Response({"message": "Tranzaksiya o'chirildi va balans tiklandi"}, status=status.HTTP_204_NO_CONTENT)