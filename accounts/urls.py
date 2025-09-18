from django.urls import path
from .views import load_users, delete_user

urlpatterns = [
    path('', load_users, name='load_users'),
    path('delete/<int:user_id>/', delete_user, name='delete_user'),
]