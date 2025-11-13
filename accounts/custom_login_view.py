from allauth.account.views import LoginView
from accounts.forms import CustomLoginForm
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import get_user_model

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    def form_valid(self, form):
        user = form.user
        if hasattr(user, 'is_blocked') and user.is_blocked:
            messages.error(self.request, "Your account is blocked. Please contact an administrator.")
            return redirect(reverse('account_login'))
        return super().form_valid(form)
