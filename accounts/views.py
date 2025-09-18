from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_POST

def load_users(request):
    users = get_user_model().objects.all()
    return render(request, 'account/users-list.html', {'users': users})

@user_passes_test(lambda u: u.is_staff)
@require_POST
def delete_user(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    if not user.is_superuser:
        user.delete()
    return redirect('users-list')