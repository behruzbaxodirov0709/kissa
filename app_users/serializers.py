import random, re
from datetime import timedelta
from rest_framework import serializers
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import get_user_model, authenticate
from .models import CustomUser, EmailConfirmationCode, Account



CustomUser = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "language", "password", "confirm_password"]

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({
                "confirm_password": "Kiritilgan parollar bir-biriga mos kelmadi."
            })

        errors = []
        if len(password) < 8:
            errors.append("Parol kamida 8 ta belgidan iborat bo'lishi kerak.")
        if not any(char.isdigit() for char in password):
            errors.append("Parolda kamida bitta raqam qatnashishi kerak.")
        if not any(char.isalpha() for char in password):
            errors.append("Parolda kamida bitta harf qatnashishi kerak.")

        if errors:
            raise serializers.ValidationError({"password": errors})

        return attrs
    
    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern=pattern, string=email):
            raise serializers.ValidationError(
                detail={
                    "message":"Email to'g'ri formatda emas!"
                }
            )

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                detail={
                    "message":"Ushbu email allaqachon ro'yxatdan o'tgan!"
                }
            )
        
        return email


    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = CustomUser.objects.create_user(**validated_data)

        code = str(random.randint(100000, 999999))
        EmailConfirmationCode.objects.create(user=user, code=code)

        send_mail(
            subject="Kissa — Tasdiqlash kodi",
            message=f"Sizning tasdiqlash kodingiz: {code}",
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'bekzodovich0709@gmail.com'),
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs.get("email"), password=attrs.get("password"))
        if user is None:
            raise serializers.ValidationError(
                detail={
                    "message":"Email yoki parol noto'g'ri"
                }
            )
        if not user.is_verified:
            raise serializers.ValidationError(
                detail={
                    "message":"Email hali tasdiqlanmagan. Iltimos, OTP kodini tasdiqlang."
                }
            )

        attrs["user"] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "email", "language", "is_verified"]
        read_only_fields = ["id", "email", "is_verified"]


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')  

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                {"email":"Bu email hali ro'yxatdan o'tkazilmagan"}
            )

        last_send_code = EmailConfirmationCode.objects.filter(user=user, code=code, is_used=False).last()

        if last_send_code is None:
            raise serializers.ValidationError(
                {"code":"Kod noto'g'ri"}
            )

        if not last_send_code.is_valid():
            raise serializers.ValidationError(
                {"code":"Kodni muddati o'tgan"}
            )

        if user.is_verified == True:
            raise serializers.ValidationError(
                {"user":"User allaqachon ro'yxatdan o'tgan"}
            )
        

        attrs['user'] = user
        attrs['last_send_code'] = last_send_code

        return attrs


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                detail={
                    "message":"Bunday email foydalanuvchi topilmadi!"
                }
            )

        if user.is_verified:
           raise serializers.ValidationError(
                detail={
                    "message":"Ushbu email allaqachon tasdiqlangan"
                }
            )

        email_object = EmailConfirmationCode.objects.filter(user=user).order_by('-created_at').first()

        if email_object and email_object.is_valid():
            now = timezone.now()
            all_seconds = int((email_object.expired_at - now).total_seconds())
            minutes = all_seconds // 60
            seconds = all_seconds % 60

            raise serializers.ValidationError(
                detail={
                    "message":f"Yangi kodni {minutes:02d}:{seconds:02d} dan so'ng qayta so'rashingiz mumkin"
                }
            )

        return email