from django.urls import path
from .views import products_list, create_sale, view_sales, delete_sale

urlpatterns = [
    path('products/', products_list, name='products_list'),
    path('create/', create_sale, name='create_sale'),
    path('view/', view_sales, name='view_sales'),
    path('delete/<int:sale_id>/', delete_sale, name='delete_sale'),
]
