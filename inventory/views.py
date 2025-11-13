import json
import pytz
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
)
from .models import Storeroom

from inventory.models import RawItem
from .models import Ingredient
from .forms import IngredientForm, StockForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import RawItem, Purchase, StoreroomItem
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from .models import Storeroom
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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

# RawItem Views
class RawItemListView(ListView):
    model = RawItem
    template_name = 'inventory/rawitem_list.html'

class RawItemDetailView(DetailView):
    model = RawItem
    template_name = 'inventory/rawitem_detail.html'

class RawItemCreateView(CreateView):
    model = RawItem
    fields = '__all__'
    template_name = 'inventory/rawitem_form.html'
    success_url = reverse_lazy('rawitem-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            from activitylog.utils import log_activity
            user = self.request.user
            raw_item = self.object
            log_activity(user, 'RAW_ITEM', raw_item.id, 'Created raw item')
        except Exception as e:
            print(f"[ERROR] Failed to log raw item creation: {e}")
        return response

class RawItemUpdateView(UpdateView):
    model = RawItem
    fields = '__all__'
    template_name = 'inventory/rawitem_form.html'
    success_url = reverse_lazy('rawitem-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            from activitylog.utils import log_activity
            user = self.request.user
            raw_item = self.object
            log_activity(user, 'RAW_ITEM', raw_item.id, 'Edited raw item')
        except Exception as e:
            print(f"[ERROR] Failed to log raw item edit: {e}")
        return response

class RawItemDeleteView(DeleteView):
    model = RawItem
    template_name = 'inventory/rawitem_confirm_delete.html'
    success_url = reverse_lazy('rawitem-list')

def purchase_create_view(request):
    raw_items = [
        {
            'id': item.id,
            'name': item.name,
            'uom': item.unit_of_measurement,
            'price': float(item.price),
        }
        for item in RawItem.objects.filter(display=True)
    ]

    if request.method == 'POST':
        supplier_name = request.POST.get('supplier_name')
        invoice_number = request.POST.get('invoice_number')
        tz = pytz.timezone('Asia/Shanghai')  # GMT+8
        datetime_val = timezone.now().astimezone(tz)
        total = 0
        purchase_items = []

        # Collect raw item purchases
        for key in request.POST:
            if key.startswith('raw_item_'):
                idx = key.split('_')[-1]
                raw_item_id = request.POST.get(f'raw_item_{idx}')
                qty = request.POST.get(f'qty_{idx}')
                price = request.POST.get(f'price_{idx}')
                expiration = request.POST.get(f'expiration_{idx}')
                if raw_item_id and qty and price:
                    try:
                        raw_item = RawItem.objects.get(pk=raw_item_id)
                        qty = float(qty)
                        price = float(price)
                        total += price * qty
                        purchase_items.append({
                            'raw_item': raw_item,
                            'qty': qty,
                            'price': price,
                            'expiration': expiration,
                        })
                    except RawItem.DoesNotExist:
                        continue

        # Create Purchase
        purchase = Purchase.objects.create(
            supplier_name=supplier_name,
            invoice_number=invoice_number,
            datetime=datetime_val,
            total=total,
            user=request.user,
            display=True
        )
        try:
            from activitylog.utils import log_activity
            log_activity(request.user, 'PURCHASE', purchase.id, 'Created purchase')
        except Exception as e:
            print(f"[ERROR] Failed to log purchase creation: {e}")

        from datetime import datetime
        for item in purchase_items:
            expiration_date = None
            if 'expiration' in item and item['expiration']:
                try:
                    expiration_date = datetime.strptime(item['expiration'], "%Y-%m-%d").date()
                except Exception:
                    expiration_date = None
            StoreroomItem.objects.create(
                raw_item_id=item['raw_item'].id,
                po_id=purchase.id,
                price=item['price'],
                quantity=item['qty'],
                expiration_date=expiration_date,
                display=True
            )
            storeroom_entry, created = Storeroom.objects.get_or_create(
                raw_item_id=item['raw_item'].id,
                defaults={'quantity': Decimal(str(item['qty'])), 'display': True}
            )
            if not created:
                storeroom_entry.quantity += Decimal(str(item['qty']))
                storeroom_entry.save()
        return redirect('purchase-add')

    context = {
        'raw_items_json': json.dumps(raw_items),
    }
    return render(request, 'inventory/purchase_form.html', context)
    
def storeroom_view(request):
    from datetime import date, timedelta
    storeroom_items = StoreroomItem.objects.all()
    today = date.today()
    soon_threshold = today + timedelta(days=7)
    items = []
    raw_item_cache = {}
    expired_items = []
    soon_items = []
    for entry in storeroom_items:
        status = 'normal'
        if entry.expiration_date:
            if entry.expiration_date < today:
                status = 'expired'
                expired_items.append(entry)
            elif entry.expiration_date <= soon_threshold:
                status = 'soon'
                soon_items.append(entry)
        # Get raw item name
        raw_item = raw_item_cache.get(entry.raw_item_id)
        if raw_item is None:
            try:
                raw_item = RawItem.objects.get(id=entry.raw_item_id)
                raw_item_cache[entry.raw_item_id] = raw_item
            except RawItem.DoesNotExist:
                raw_item = None
        items.append({
            'entry': entry,
            'status': status,
            'raw_item': raw_item
        })
    # Show both warnings if both exist
    if expired_items:
        messages.warning(request, f"There are {len(expired_items)} expired item(s) in the storeroom.")
    if soon_items:
        messages.warning(request, f"There are {len(soon_items)} item(s) expiring within 7 days.")
    return render(request, 'inventory/storeroom.html', {'storeroom_list': items})

@csrf_exempt
def storeroom_toggle_display(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        item_id = data.get('id')
        display = data.get('display')
        try:
            entry = Storeroom.objects.get(pk=item_id)
            entry.display = display
            entry.save()
            return JsonResponse({'success': True})
        except Storeroom.DoesNotExist:
            return JsonResponse({'success': False}, status=404)
    return JsonResponse({'success': False}, status=400)

from .models import Transfer, TransferItem, Storeroom
from django.contrib import messages

def transfer_create_view(request):
    print('[DEBUG] transfer_create_view called')
    storeroom_list = Storeroom.objects.select_related('raw_item').filter(display=True)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        tz = pytz.timezone('Asia/Shanghai')
        datetime_val = timezone.now().astimezone(tz)
        user = request.user

        transfer_items = []
        for key in request.POST:
            if key.startswith('storeroom_item_'):
                idx = key.split('_')[-1]
                storeroom_item_id = request.POST.get(f'storeroom_item_{idx}')
                qty = request.POST.get(f'qty_{idx}')
                if storeroom_item_id and qty:
                    try:
                        storeroom_entry = Storeroom.objects.get(pk=storeroom_item_id)
                        qty = Decimal(str(qty))
                        if qty > storeroom_entry.quantity:
                            messages.error(request, f"Cannot transfer more than available ({storeroom_entry.quantity}) for {storeroom_entry.raw_item.name}.")
                            return render(request, 'inventory/transfer_form.html', {'storeroom_list': storeroom_list})
                        transfer_items.append({
                            'storeroom_entry': storeroom_entry,
                            'qty': qty,
                        })
                    except Storeroom.DoesNotExist:
                        continue

        transfer = Transfer.objects.create(
            datetime=datetime_val,
            reason=reason,
            user=user,
            display=True
        )
        from activitylog.utils import log_activity
        log_activity(user, 'TRANSFER', transfer.id, 'Created transfer')

        for item in transfer_items:
            TransferItem.objects.create(
                transfer_id=transfer.id,
                raw_item_id=item['storeroom_entry'].raw_item.id,
                quantity=item['qty'],
                display=True
            )
            # Deduct from storeroom
            item['storeroom_entry'].quantity -= item['qty']
            item['storeroom_entry'].save()

        messages.success(request, "Transfer created successfully!")
        return redirect('storeroom')

    return render(request, 'inventory/transfer_form.html', {'storeroom_list': storeroom_list})