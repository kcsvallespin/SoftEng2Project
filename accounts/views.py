from django.contrib.auth import get_user_model
from django.shortcuts import render

def load_users(request):
    users = get_user_model().objects.all()
    return render(request, 'account/users-list.html', {'users': users})
