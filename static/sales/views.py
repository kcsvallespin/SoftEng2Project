import json
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Prefetch
from django.utils import timezone
from .models import Saleitems, Sales
from menu.models import Items, ItemVariants

def display_products(request):
    items = Items.objects.prefetch_related(
        Prefetch('itemvariants', queryset=ItemVariants.objects.order_by('sku'))
    )
    return render(request, 'sales/create-sales.html', {'items': items})

def display_sale(request, sale_id):
    items = Items.objects.prefetch_related(
        Prefetch('itemvariants', queryset=ItemVariants.objects.order_by('sku'))
    )
    sale = Sales.objects.prefetch_related('saleitems').get(pk=sale_id)
    return render(request, 'sales/edit-sales.html', {'items': items, 'sale': sale})

def create_sale(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=403)
        try:
            data = json.loads(request.body)
            total_price = sum(item['price'] * item['quantity'] for item in data)
            user = get_user_model().objects.get(pk=request.user.pk)
            new_sale = Sales.objects.create(user=user, total_price=total_price, datetime=timezone.now())
            for item in data:
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
            incoming_item_variant_ids = set()
            for item in data:
                item_variant_id = item['item_variant_id']
                quantity = item['quantity']
                price = item['price']
                incoming_item_variant_ids.add(item_variant_id)
                item_variant = ItemVariants.objects.get(pk=item_variant_id)
                saleitem, created = Saleitems.objects.get_or_create(
                    sale = sale,
                    item_variant = item_variant,
                    defaults={'price': price, 'quantity': quantity}
                )
                if not created:
                    saleitem.price = price
                    saleitem.quantity = quantity
                    saleitem.save()
            sale.saleitems.exclude(item_variant_id__in=incoming_item_variant_ids).delete()   
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
