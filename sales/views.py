import json
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Prefetch
from django.utils import timezone
from .models import Saleitems, Sales
from menu.models import Items, ItemVariants

def display_products(request):
    from django.conf import settings as djsettings
    items = Items.objects.prefetch_related(
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
            total_price = sum(item['price'] * item['quantity'] for item in items)
            user = get_user_model().objects.get(pk=request.user.pk)
            new_sale = Sales.objects.create(
                user=user,
                total_price=total_price,
                datetime=timezone.now(),
                invoice_number=invoice_number,
                tin=tin,
                payment_type=payment_type
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
            total_price = sum(item['price'] * item['quantity'] for item in data)
            incoming_saleitem_ids = set()
            for item in data:
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
            sale.total_price = total_price
            sale.save()
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

def refund_sale(request, sale_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'User not authorized'}, status=403)
    if request.method == "POST":
        try:
            sale = Sales.objects.get(pk=sale_id)
            saleitem_count = sale.saleitems.count()
            #    return render(request, 'sales/refund.html', {'sale': sale, 'saleitem_count': saleitem_count})
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# check if sale was made online
# if online, saleitem_count should be reduced
# otherwise, saleitem_count should be maintained
