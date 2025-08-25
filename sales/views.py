import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Prefetch
from .models import Products, Categories, Saleitems, Sales

def display_products(request):
    products = Products.objects.prefetch_related(
        Prefetch('categories_set', queryset=Categories.objects.order_by('category_name'))).order_by('name')
    return render(request, 'sales/create-sales.html', {'products': products})

def display_sale(request, sale_id):
    products = Products.objects.prefetch_related(
        Prefetch('categories_set', queryset=Categories.objects.order_by('category_name'))).order_by('name')
    sale = Sales.objects.prefetch_related('saleitems_set__category').get(pk=sale_id)
    print(sale)
    return render(request, 'sales/edit-sales.html', {'products': products, 'sale': sale})


def create_sale(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=403)
        try:
            data = json.loads(request.body)
            total_price = sum(item['price'] * item['quantity'] for item in data)
            user = get_user_model().objects.get(pk=request.user.pk)
            new_sale = Sales.objects.create(user=user, total_price=total_price)
            for item in data:
                category_id = item['categoryId']
                category = Categories.objects.get(pk=category_id)
                Saleitems.objects.create(
                    sale = new_sale,
                    category = category,
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
            incoming_category_ids = set()
            for item in data:
                category_id = item['categoryId']
                quantity = item['quantity']
                price = item['price']
                incoming_category_ids.add(category_id)
                category = Categories.objects.get(pk=category_id)
                saleitem, created = Saleitems.object.get_or_create(
                    sale = sale,
                    category = category,
                    defaults={'price': price, 'quantity': quantity}
                )
                if not created:
                    saleitem.price = price
                    saleitem.quantity = quantity
                    saleitem.save()
            sale.saleitems_set.exclude(category_id__in=incoming_category_ids).delete()   
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
    
    sales = Sales.objects.prefetch_related('saleitems_set')
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

def get_sale(request, sale_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'User not authorized'}, status=403)

    display_products(request)

    try:
        sale = Sales.objects.prefetch_related('saleitems_set').get(pk=sale_id)
        data = {
            'id': sale.id,
            'user': sale.user.username,
            'total_price': sale.total_price,
            'datetime': sale.datetime,
            'items': [
                {
                    'category_id': item.category.id,
                    'category_name': item.category.category_name,
                    'price': item.price,
                    'quantity': item.quantity
                } for item in sale.saleitems_set.all()
            ]
        }
        return JsonResponse(data)
    except Sales.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Sale not found'}, status=404)

def edit_sale(request, sale_id):
    return render(request, 'sales/edit-sales.html', {'sale_id': sale_id})
