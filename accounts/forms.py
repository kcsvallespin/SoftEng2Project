from django import forms
from django.contrib.auth import get_user_model
from allauth.account.forms import LoginForm as AllauthLoginForm
class CustomLoginForm(AllauthLoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove password reset help text
        if 'login' in self.fields:
            self.fields['login'].help_text = ''
        self.fields['password'].help_text = ''

    def get_context(self):
        context = super().get_context()
        # Remove password reset link from context if present
        context['password_reset_url'] = None
        return context

class UsernamePasswordResetForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150)

    def get_users(self):
        User = get_user_model()
        username = self.cleaned_data.get('username')
        return User.objects.filter(username__iexact=username)
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(AdminUserCreationForm):

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
        )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
        )
