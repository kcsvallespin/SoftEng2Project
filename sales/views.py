import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Prefetch
from .models import Products, Categories, Saleitems, Sales

def products_list(request):
    products = Products.objects.prefetch_related(
        Prefetch('categories_set', queryset=Categories.objects.order_by('category_name'))).order_by('name')
    return render(request, 'sales/create-sales.html', {'products': products})

@csrf_exempt
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
