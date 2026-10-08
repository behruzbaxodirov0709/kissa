from django.contrib import admin
from .models import CustomUser, EmailConfirmationCode, Account, Category, Transactions



# @admin.register(CustomUser)
# class UserAdmin()


@admin.register(EmailConfirmationCode)
class EmailConfirmationCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'expires_at')
    search_fields = ('user__username', 'user__username', 'code', 'created_at', 'expired_at')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'type', 'balance', 'currency', 'created_at')
    list_filter = ('type', 'currency')
    search_fields = ('name', 'user__email', 'user__email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'type')
    list_filter = ('user', 'type')
    search_fields = ('name', 'user__email', 'user__username')


@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'account', 'category', 'type', 'amount', 'date', 'created_at')
    list_filter = ('type', 'date')
    search_fields = ('user__username', 'user__email', 'description')