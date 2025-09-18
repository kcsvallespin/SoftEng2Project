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

    # Home page
    path('home/', views.HomePageView.as_view(), name='inventory-home'),
]