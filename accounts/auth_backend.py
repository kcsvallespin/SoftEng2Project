from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class BlockedUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        user = None
        # Support login by username or email
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Try email
                user = User.objects.filter(email__iexact=username).first()
        if user:
            if getattr(user, 'is_blocked', False):
                return None
            if user.check_password(password):
                return user
        return None
