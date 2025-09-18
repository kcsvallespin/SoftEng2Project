from django import forms
from .models import Ingredient

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

class StockForm(forms.Form):
    amount = forms.IntegerField(min_value=1, label="Amount")

def form_valid(self, form):
    ingredient = self.get_object()
    amount = form.cleaned_data['amount']
    if amount > ingredient.quantity:
        form.add_error('amount', f'Cannot stock out more than current amount ({ingredient.quantity}).')
        return self.form_invalid(form)