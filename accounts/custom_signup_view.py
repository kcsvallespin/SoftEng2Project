from allauth.account.views import SignupView
from django.urls import reverse_lazy
from django.shortcuts import redirect

class CustomSignupView(SignupView):
    redirect_authenticated_user = False

    def dispatch(self, request, *args, **kwargs):
        # Correctly call super().dispatch
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('home')
