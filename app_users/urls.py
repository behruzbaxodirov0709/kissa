from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # ==================== 1. AUTHENTICATION & PROFILE ====================
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', views.ResendOTPView.as_view(), name='resend-otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # ==================== 2. PASSWORD RESET (3-Bosqich) ====================
    path('password-reset/request/', views.PasswordResetRequestAPIView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', views.PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),

    # ==================== 3. ACCOUNTS (Hamyonlar) ====================
    path('accounts/', views.AccountListAPIView.as_view(), name='account-list'),
    path('accounts/create/', views.AccountCreateAPIView.as_view(), name='account-create'),
    path('accounts/<int:pk>/', views.AccountDetailAPIView.as_view(), name='account-detail'),
    path('accounts/<int:pk>/update/', views.AccountUpdateAPIView.as_view(), name='account-update'),
    path('accounts/<int:pk>/delete/', views.AccountDeleteAPIView.as_view(), name='account-delete'),

    # ==================== 4. CATEGORIES (Kategoriyalar) ====================
    path('categories/', views.CategoryListAPIView.as_view(), name='category-list'),
    path('categories/create/', views.CategoryCreateAPIView.as_view(), name='category-create'),
    path('categories/<int:pk>/', views.CategoryDetailAPIView.as_view(), name='category-detail'),
    path('categories/<int:pk>/update/', views.CategoryUpdateAPIView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteAPIView.as_view(), name='category-delete'),

    # ==================== 5. TRANSACTIONS (Tranzaksiyalar) ====================
    path('transactions/', views.TransactionListAPIView.as_view(), name='transaction-list'),
    path('transactions/create/', views.TransactionCreateAPIView.as_view(), name='transaction-create'),
    path('transactions/<int:pk>/', views.TransactionDetailAPIView.as_view(), name='transaction-detail'),
    path('transactions/<int:pk>/delete/', views.TransactionDeleteAPIView.as_view(), name='transaction-delete'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # Profile Endpoints
    path('profile/', views.UserProfileAPIView.as_view(), name='user-profile'),
    path('profile/change-password/', views.ChangePasswordAPIView.as_view(), name='change-password'),
]