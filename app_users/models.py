from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime 
from django.utils import timezone
from rest_framework import settings



class CustomUser(AbstractUser):
    LANGUAGE_CHOICES = (
        ('uz', 'Uzbek'),
        ('ru', 'Russian'),
        ('en', 'English'),
    )

    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default="uz")


    def __str__(self):
        return self.username


class EmailConfirmationCode(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name="confirmation_codes")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expired_at:
            self.expired_at = self.created_at + datetime.timedelta(minutes=settings.EMAIL_EXPIRATION_TIME)
        return super().save(*args, **kwargs)

    
    def is_valid(self):
        return timezone.now() <= self.expired_at


class Account(models.Model):
    ACCOUNT_TYPES = (
        ("cash", "naqd pul"),
        ("card", "karta"),
        ("currency", "valyuta"),
    )

    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name="accounts")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default="cash")
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default="UZS")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}  ({self.type})"


class Category(models.Model):
    CATEGORY_TYPES = (
        ('income', 'kirim'),
        ('expense', 'chiqim'),
    )

    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPES)

    def __str__(self):
        return f"{self.user.username} - ({self.type})"


class Transactions(models.Model):
    TRANSACTION_TYPES = (
            ('income', 'kirim'),
            ('expense', 'chiqim'),
        )

    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name="transactions")
    account = models.ForeignKey(to=Account, on_delete=models.CASCADE, related_name="transactions")
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name="transactions")
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField(default=timezone.now())
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.account.type} - {self.amount}"

