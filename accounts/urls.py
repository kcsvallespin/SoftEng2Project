from django.urls import path
from .views import load_users, delete_user, create_user, block_user, password_reset_by_username

urlpatterns = [
    path('', load_users, name='load_users'),
    path('delete/<int:user_id>/', delete_user, name='delete_user'),
    path('create/', create_user, name='create_user'),
    path('block/<int:user_id>/', block_user, name='block_user'),
    path('password-reset/', password_reset_by_username, name='password_reset_by_username'),
]