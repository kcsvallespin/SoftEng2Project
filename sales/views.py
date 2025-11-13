import json
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Prefetch, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Saleitems, Sales
from menu.models import Items, ItemVariants

def display_products(request):
    from django.conf import settings as djsettings
    items = Items.objects.filter(is_active=True).prefetch_related(
        Prefetch('itemvariants', queryset=ItemVariants.objects.order_by('sku'))
    )
    return render(request, 'sales/create-sales.html', {
        'items': items,
        'MEDIA_URL': getattr(djsettings, 'MEDIA_URL', '/media/')
    })

def display_sale(request, sale_id):
    items = Items.objects.prefetch_related(
        Prefetch('itemvariants', queryset=ItemVariants.objects.order_by('sku'))
    )
    sale = Sales.objects.prefetch_related('saleitems__item_variant__item__itemvariants').get(pk=sale_id)
    # Attach .variants to each saleitem for template dropdown
    for saleitem in sale.saleitems.all():
        saleitem.variants = saleitem.item_variant.item.itemvariants.all()
    # Build itemVariantsMap for JS
    import json as pyjson
    item_variants_map = {}
    for menu_item in items:
        item_variants_map[menu_item.item_id] = [
            {
                'variant_id': variant.variant_id,
                'name': variant.sku if variant.sku else f"Variant {variant.variant_id}",
                'variation': str(getattr(variant, 'variation', '')),
                'price': str(variant.price)
            }
            for variant in menu_item.itemvariants.all()
        ]
    item_variants_json = pyjson.dumps(item_variants_map)
    return render(request, 'sales/edit-sales.html', {
        'items': items,
        'sale': sale,
        'item_variants_json': item_variants_json
    })
    return render(request, 'sales/edit-sales.html', {'items': items, 'sale': sale})

def create_sale(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=403)
        try:
            payload = json.loads(request.body)
            if isinstance(payload, list):
                items = payload
                invoice_number = None
                tin = None
                payment_type = None
            else:
                items = payload.get('items', [])
                invoice_number = payload.get('invoice_number')
                tin = payload.get('tin')
                payment_type = payload.get('payment_type')
                customer_name = payload.get('customer_name')
                reference_number = payload.get('reference_number')
            total_price = sum(item['price'] * item['quantity'] for item in items)
            user = get_user_model().objects.get(pk=request.user.pk)
            new_sale = Sales.objects.create(
                user=user,
                total_price=total_price,
                datetime=timezone.now(),
                invoice_number=invoice_number,
                tin=tin,
                payment_type=payment_type,
                customer_name=customer_name,
                reference_number=reference_number
            )
            for item in items:
                item_variant_id = item['item_variant_id']
                item_variant = ItemVariants.objects.get(pk=item_variant_id)
                Saleitems.objects.create(
                    sale = new_sale,
                    item_variant = item_variant,
                    price = item['price'],
                    quantity = item['quantity']
                )
            # Log activity for sale creation
            try:
                from activitylog.utils import log_activity
                log_activity(request.user, 'sale_creation', new_sale.pk, 'created')
            except Exception as e:
                print(f"[ERROR] Activity logging failed: {e}")
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'invalid method'}, status=405)

def edit_sale(request, sale_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=403)
        try:
            sale = Sales.objects.get(pk=sale_id)
            data = json.loads(request.body)
            items = data.get('items', data)  # support both array and dict
            total_price = sum(item['price'] * item['quantity'] for item in items)
            incoming_saleitem_ids = set()
            for item in items:
                saleitem_id = item.get('saleitem_id')
                quantity = item['quantity']
                price = item['price']
                incoming_saleitem_ids.add(saleitem_id)
                try:
                    saleitem = Saleitems.objects.get(pk=saleitem_id, sale=sale)
                except Saleitems.DoesNotExist:
                    continue
                saleitem.price = price
                saleitem.quantity = quantity
                saleitem.save()
            sale.saleitems.exclude(pk__in=incoming_saleitem_ids).delete()
            # Update transaction fields
            sale.total_price = total_price
            sale.invoice_number = data.get('invoice_number', sale.invoice_number)
            sale.tin = data.get('tin', sale.tin)
            sale.payment_type = data.get('payment_type', sale.payment_type)
            sale.customer_name = data.get('customer_name', sale.customer_name)
            sale.reference_number = data.get('reference_number', sale.reference_number)
            sale.save()
            # Log activity for sale edit
            from activitylog.utils import log_activity
            log_activity(request.user, 'sale_edit', sale.pk, 'edited')
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'invalid method'}, status=405)

def view_sales(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=403)
    
    sales = Sales.objects.prefetch_related('saleitems').all()
    if request.user.is_staff:
        sales = sales.order_by('-datetime')
    else:
        sales = sales.filter(user=request.user).order_by('-datetime')
    return render(request, 'sales/view-sales.html', {'sales': sales})

def delete_sale(request, sale_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'User not authorized'}, status=403)
    if request.method == "POST":
        selected = Sales.objects.get(pk=sale_id)
        try:
            selected.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def sales_history(request):
    products = ItemVariants.objects.filter(item__is_active=True).all()
    product_id = request.GET.get('product_id')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)

    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            pass
    
    selected = None
    sales_by_day = []
    total_sold = 0

    if product_id:
        try:
            selected = ItemVariants.objects.get(pk=product_id)
        except ItemVariants.DoesNotExist:
            selected = None

        if selected:
            sales_by_day_qs = (
                Saleitems.objects
                .filter(item_variant=selected, sale__datetime__range=(start_date, end_date))
                .annotate(sale_date=TruncDate('sale__datetime'))
                .values('sale_date')
                .annotate(total_sold=Sum('quantity'))
                .order_by('sale_date')
            )
            sales_by_day = list(sales_by_day_qs)

            total_sold = (
                Saleitems.objects
                .filter(item_variant=selected, sale__datetime__range=(start_date, end_date))
                .aggregate(total_sold=Sum('quantity'))['total_sold'] or 0
            )

    context = {
        'products': products,
        'selected': selected,
        'sales_by_day': sales_by_day,
        'total_sold': total_sold,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'sales/sales-history.html', context)

