from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from .models import Ingredient, Supplier
from django.views.generic import FormView
from .forms import IngredientForm
from .forms import StockForm


# Ingredient Views
class IngredientListView(ListView):
    model = Ingredient
    class Meta:
        db_table = 'ingredients'
    template_name = 'inventory/ingredient_list.html'

class IngredientDetailView(DetailView):
    model = Ingredient
    template_name = 'inventory/ingredient_detail.html'

class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'inventory/ingredient_form.html'
    success_url = reverse_lazy('ingredient-list')

class IngredientUpdateView(UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'inventory/ingredient_form.html'
    success_url = reverse_lazy('ingredient-list')

class IngredientStockInView(FormView):
    template_name = 'inventory/ingredient_stock_in.html'
    form_class = StockForm

    def form_valid(self, form):
        ingredient = get_object_or_404(Ingredient, pk=self.kwargs['pk'])
        ingredient.quantity += form.cleaned_data['amount']
        ingredient.save()
        return redirect('ingredient-list')
    
class IngredientStockOutView(FormView):
    template_name = 'inventory/ingredient_stock_out.html'
    form_class = StockForm

    def form_valid(self, form):
        ingredient = get_object_or_404(Ingredient, pk=self.kwargs['pk'])
        amount = form.cleaned_data['amount']
        if ingredient.quantity >= amount:
            ingredient.quantity -= amount
            ingredient.save()
        # Optionally, handle insufficient stock here
        return redirect('ingredient-list')

class IngredientDeleteView(DeleteView):
    model = Ingredient
    template_name = 'inventory/ingredient_confirm_delete.html'
    success_url = reverse_lazy('ingredient-list')

    def form_valid(self, form):
        ingredient = get_object_or_404(Ingredient, pk=self.kwargs['pk'])
        amount = form.cleaned_data['amount']
        if ingredient.quantity >= amount:
            ingredient.quantity -= amount
            ingredient.save()
        # Optionally, handle insufficient stock here
        return redirect('ingredient-list')

# Supplier Views
class SupplierListView(ListView):
    model = Supplier
    class Meta:
        db_table = 'suppliers'
    template_name = 'inventory/supplier_list.html'

class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'inventory/supplier_detail.html'

class SupplierCreateView(CreateView):
    model = Supplier
    fields = '__all__'
    template_name = 'inventory/supplier_form.html'
    success_url = reverse_lazy('supplier-list')

class SupplierUpdateView(UpdateView):
    model = Supplier
    fields = '__all__'
    template_name = 'inventory/supplier_form.html'
    success_url = reverse_lazy('supplier-list')

class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = 'inventory/supplier_confirm_delete.html'
    success_url = reverse_lazy('supplier-list')

class HomePageView(TemplateView):
    template_name = 'inventory/home.html'