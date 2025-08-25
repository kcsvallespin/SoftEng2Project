from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from .models import CustomUser
#ADDED BY 'WARREN'
from allauth.account.forms import SignupForm
from django import forms
#---------------------------------------

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

#EVEN THIS IS MINE
class CustomSignupForm(SignupForm):
    username = forms.CharField(max_length=150, label='Username', required=False, widget=forms.TextInput(attrs={'placeholder': 'Username'}))

    def save(self, request):
        user = super().save(request)
        return user
#-------------------------------------