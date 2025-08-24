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