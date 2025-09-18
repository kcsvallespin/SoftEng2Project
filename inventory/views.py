from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
)
from .models import Ingredient
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

    def get_object(self):
        return Ingredient.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context

    def form_valid(self, form):
        ingredient = get_object_or_404(Ingredient, pk=self.kwargs['pk'])
        ingredient.quantity += form.cleaned_data['amount']
        ingredient.save()
        return redirect('ingredient-list')
    
class IngredientStockOutView(FormView):
    template_name = 'inventory/ingredient_stock_out.html'
    form_class = StockForm
    success_url = reverse_lazy('ingredient-list')

    def get_object(self):
        return Ingredient.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context
    
    def form_valid(self, form):
        ingredient = self.get_object()
        amount = form.cleaned_data['amount']
        if amount > ingredient.quantity:
            form.add_error('amount', f'Cannot stock out more than current amount ({ingredient.quantity}).')
            return self.form_invalid(form)
        if ingredient.quantity >= amount:
            ingredient.quantity -= amount
            ingredient.save()
        return super().form_valid(form)

class IngredientDeleteView(StaffRequiredMixin, DeleteView):
    model = Ingredient
    template_name = 'inventory/ingredient_confirm_delete.html'
    success_url = reverse_lazy('ingredient-list')

class HomePageView(StaffRequiredMixin, TemplateView):
    template_name = 'inventory/home.html'