import random, re
from rest_framework import serializers
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import CustomUser, EmailConfirmationCode, Account



from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError




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
        
        return email


    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = CustomUser.objects.create_user(**validated_data)

        code = str(random.randint(100000, 999999))
        EmailConfirmationCode.objects.create(user=user, code=code)

        send_mail(
            subject="Kissa — Tasdiqlash kodi",
            message=f"Sizning tasdiqlash kodingiz: {code}",
            from_email='bekzodovich0709@gmail.com',
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user


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

        attrs['user'] = user
        attrs['last_send_code'] = last_send_code

        return attrs