from django.urls import path
from .views import create_item, view_items, edit_item

urlpatterns = [
    path('create/', create_item, name='create_item'),
    path('view/', view_items, name='view_items'),
    path('edit/<int:item_id>/', edit_item, name='edit_item'),
    
]
