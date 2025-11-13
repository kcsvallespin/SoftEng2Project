from django.urls import path
from allauth.account.views import (
    # LoginView, 
    LogoutView, PasswordChangeView, PasswordSetView,
    PasswordResetView, PasswordResetDoneView, PasswordResetFromKeyView, PasswordResetFromKeyDoneView,
    EmailView, EmailVerificationSentView, ConfirmEmailView,
)
from accounts.custom_signup_view import CustomSignupView

urlpatterns = [
    # path('login/', LoginView.as_view(), name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
    path('password/change/', PasswordChangeView.as_view(), name='account_change_password'),
    path('password/set/', PasswordSetView.as_view(), name='account_set_password'),
    path('password/reset/', PasswordResetView.as_view(), name='account_reset_password'),
    path('password/reset/done/', PasswordResetDoneView.as_view(), name='account_reset_password_done'),
    path('password/reset/key/<uidb36>/<key>/', PasswordResetFromKeyView.as_view(), name='account_reset_password_from_key'),
    path('password/reset/key/done/', PasswordResetFromKeyDoneView.as_view(), name='account_reset_password_from_key_done'),
    path('signup/', CustomSignupView.as_view(), name='account_signup'),
    path('email/', EmailView.as_view(), name='account_email'),
    path('confirm-email/', EmailVerificationSentView.as_view(), name='account_email_verification_sent'),
    path('confirm-email/<key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
]
