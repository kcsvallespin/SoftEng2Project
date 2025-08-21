import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from .models import Products, Categories, Saleitems, Sales

def products_list(request):
    products = Products.objects.all().order_by('name')
    categories = Categories.objects.all()
    return render(request, 'sales/sales.html', {'products': products, 'categories': categories})

@csrf_exempt
def create_sale(request):
    ##newSale = Sales.objects.create()

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('received data: ', data)

            total_price = sum(item['price'] * item['quantity'] for item in data)
            new_sale = Sales.objects.create(total_price=total_price, datetime=datetime.now())
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
