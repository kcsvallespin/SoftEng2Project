from django.urls import path
from .views import products_list, create_sale

urlpatterns = [
    path('', products_list, name='products_list'),
    path('create_sale/', create_sale, name='create_sale'),
]
