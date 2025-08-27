from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
)
from .models import Ingredient, Supplier
from .forms import IngredientForm, StockForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

# Ingredient Views
class IngredientListView(StaffRequiredMixin, ListView):
    model = Ingredient
    class Meta:
        db_table = 'ingredients'
    template_name = 'inventory/ingredient_list.html'

class IngredientDetailView(StaffRequiredMixin, DetailView):
    model = Ingredient
    template_name = 'inventory/ingredient_detail.html'

class IngredientCreateView(StaffRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'inventory/ingredient_form.html'
    success_url = reverse_lazy('ingredient-list')

class IngredientUpdateView(StaffRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'inventory/ingredient_form.html'
    success_url = reverse_lazy('ingredient-list')

class IngredientStockInView(StaffRequiredMixin, FormView):
    template_name = 'inventory/ingredient_stock_in.html'
    form_class = StockForm

    def form_valid(self, form):
        ingredient = get_object_or_404(Ingredient, pk=self.kwargs['pk'])
        ingredient.quantity += form.cleaned_data['amount']
        ingredient.save()
        return redirect('ingredient-list')
    
class IngredientStockOutView(StaffRequiredMixin, FormView):
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

class IngredientDeleteView(StaffRequiredMixin, DeleteView):
    model = Ingredient
    template_name = 'inventory/ingredient_confirm_delete.html'
    success_url = reverse_lazy('ingredient-list')

# Supplier Views
class SupplierListView(StaffRequiredMixin, ListView):
    model = Supplier
    class Meta:
        db_table = 'suppliers'
    template_name = 'inventory/supplier_list.html'

class SupplierDetailView(StaffRequiredMixin, DetailView):
    model = Supplier
    template_name = 'inventory/supplier_detail.html'

class SupplierCreateView(StaffRequiredMixin, CreateView):
    model = Supplier
    fields = '__all__'
    template_name = 'inventory/supplier_form.html'
    success_url = reverse_lazy('supplier-list')

class SupplierUpdateView(StaffRequiredMixin, UpdateView):
    model = Supplier
    fields = '__all__'
    template_name = 'inventory/supplier_form.html'
    success_url = reverse_lazy('supplier-list')

class SupplierDeleteView(StaffRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'inventory/supplier_confirm_delete.html'
    success_url = reverse_lazy('supplier-list')

class HomePageView(StaffRequiredMixin, TemplateView):
    template_name = 'inventory/home.html'