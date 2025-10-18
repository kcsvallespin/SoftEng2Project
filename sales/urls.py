from django.urls import path
from .views import display_products, create_sale, view_sales, delete_sale, edit_sale, display_sale

urlpatterns = [
    path('products/', display_products, name='display_products'),
    path('products/<int:sale_id>/', display_sale, name='display_sale'),
    path('create/', create_sale, name='create_sale'),
    path('view/', view_sales, name='view_sales'),
    path('delete/<int:sale_id>/', delete_sale, name='delete_sale'),
    path('edit/<int:sale_id>/', edit_sale, name='edit_sale'),
]
