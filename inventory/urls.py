from django.urls import path
from . import views

urlpatterns = [
    # Ingredient URLs
    path('ingredients/', views.IngredientListView.as_view(), name='ingredient-list'),
    path('ingredients/add/', views.IngredientCreateView.as_view(), name='ingredient-add'),
    path('ingredients/<int:pk>/', views.IngredientDetailView.as_view(), name='ingredient-detail'),
    path('ingredients/<int:pk>/edit/', views.IngredientUpdateView.as_view(), name='ingredient-edit'),
    path('ingredients/<int:pk>/delete/', views.IngredientDeleteView.as_view(), name='ingredient-delete'),
    path('ingredients/<int:pk>/stock-in/', views.IngredientStockInView.as_view(), name='ingredient-stock-in'),
    path('ingredients/<int:pk>/stock-out/', views.IngredientStockOutView.as_view(), name='ingredient-stock-out'),

    # Supplier URLs
    path('suppliers/', views.SupplierListView.as_view(), name='supplier-list'),
    path('suppliers/add/', views.SupplierCreateView.as_view(), name='supplier-add'),
    path('suppliers/<int:pk>/', views.SupplierDetailView.as_view(), name='supplier-detail'),
    path('suppliers/<int:pk>/edit/', views.SupplierUpdateView.as_view(), name='supplier-edit'),
    path('suppliers/<int:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier-delete'),

    # Home page
    path('home/', views.HomePageView.as_view(), name='inventory-home'),
]