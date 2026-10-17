from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from django.core.mail import send_mail  
from django.conf import settings
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, EmailConfirmationCode, Account, Category, Transaction
from . import serializers
from .pagination import CustomPageNumberPagination
import random
from drf_spectacular.utils import extend_schema, OpenApiParameter


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


@extend_schema(
    tags=['Transactions'],
    summary="Tranzaksiyalar ro'yxatini olish",
    description="Foydalanuvchining barcha kirim va chiqimlarini filter va pagination bilan olish.",
    parameters=[
        OpenApiParameter(name='type', description="income yoki expense bo'yicha filter", required=False, type=str),
        OpenApiParameter(name='start_date', description="Boshlanish sanasi (YYYY-MM-DD)", required=False, type=str),
        OpenApiParameter(name='end_date', description="Tugash sanasi (YYYY-MM-DD)", required=False, type=str),
    ]
)
class TransactionListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')

        type_param = request.query_params.get('type')
        category_id = request.query_params.get('category')
        account_id = request.query_params.get('account')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if type_param:
            queryset = queryset.filter(type=type_param)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if account_id:
            queryset = queryset.filter(account_id=account_id)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        paginator = CustomPageNumberPagination()
        page = paginator.paginate_queryset(queryset=queryset, request=request)

        if page is not None:
            serializer = serializers.TransactionSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        serializer = serializers.TransactionSerializer(queryset, many=True, context={'request': request})
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


class PasswordResetRequestAPIView(APIView):
    permission_classes = [permissions.AllowAny]  

    def post(self, request):
        serializer = serializers.PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = CustomUser.objects.get(email=email)

        
        EmailConfirmationCode.objects.filter(user=user, is_used=False).update(is_used=True)

  
        code = str(random.randint(100000, 999999))
        EmailConfirmationCode.objects.create(user=user, code=code)

        # Emailga jo'natish
        send_mail(
            subject="Kissa — Parolni tiklash kodi",
            message=f"Parolni tiklash uchun tasdiqlash kodingiz: {code}",
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'bekzodovich0709@gmail.com'),
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response(
            {"message": "Parolni tiklash kodi emailga yuborildi."},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serializers.PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        confirmation_code = serializer.validated_data['confirmation_code']
        new_password = serializer.validated_data['new_password']

     
        user.set_password(new_password)
        user.save()

        confirmation_code.is_used = True
        confirmation_code.save()

        return Response(
            {"message": "Parolingiz muvaffaqiyatli o'zgartirildi! Endi yangi parol bilan tizimga kirishingiz mumkin."},
            status=status.HTTP_200_OK
        )


class UserProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = serializers.UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = serializers.UserProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = serializers.ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response(
            {"message": "Parolingiz muvaffaqiyatli o'zgartirildi!"},
            status=status.HTTP_200_OK
        )