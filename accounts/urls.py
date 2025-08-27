from django.urls import path
from .views import load_users

urlpatterns = [
    path('', load_users, name='load_users'),
]