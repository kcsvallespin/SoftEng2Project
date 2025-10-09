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

    path('raw-items/', views.RawItemListView.as_view(), name='rawitem-list'),
    path('raw-items/add/', views.RawItemCreateView.as_view(), name='rawitem-add'),
    path('raw-items/<int:pk>/', views.RawItemDetailView.as_view(), name='rawitem-detail'),
    path('raw-items/<int:pk>/edit/', views.RawItemUpdateView.as_view(), name='rawitem-edit'),
    path('raw-items/<int:pk>/delete/', views.RawItemDeleteView.as_view(), name='rawitem-delete'), 

    path('purchases/add/', views.purchase_create_view, name='purchase-add'),

    # Home page
    path('home/', views.HomePageView.as_view(), name='inventory-home'),

    path('storeroom/', views.storeroom_view, name='storeroom'),
    path('storeroom/toggle-display/', views.storeroom_toggle_display, name='storeroom-toggle-display'),

    path('transfer/add/', views.transfer_create_view, name='transfer-add'),
]