from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Items, ItemVariants

def create_item(request):
    if request.method == 'POST':
        item_name = request.POST.get('name')
        variant_names = request.POST.getlist('variant_name[]')
        variant_prices = request.POST.getlist('variant_price[]')
        if Items.objects.filter(name=item_name).exists() is True:
            return render(request, 'menu/create-items.html', {'message': "Item with this name already exists."})

        # Create the item
        item = Items.objects.create(name=item_name)

        is_single_default_variant = (
        len(variant_names) == 1 and variant_names[0].lower() == 'default'
        )
        has_single_price = len(variant_prices) == 1

        if item_name and is_single_default_variant and has_single_price:
            # If no variants provided, create a default variant
            ItemVariants.objects.create(item=item, sku=f"{item_name}-default", price=variant_prices[0])
        # Create each variant
        else:
            for name, price in zip(variant_names, variant_prices):
                ItemVariants.objects.create(item=item, sku=name, price=price)

        #return redirect('success_or_items_list')  # Redirect somewhere appropriate

    return render(request, 'menu/create-items.html')

def view_items(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=403)
    
    items = Items.objects.prefetch_related('itemvariants').all().order_by('item_id')
    return render(request, 'menu/view-items.html', {'items': items})

def edit_item(request, item_id):
    item = get_object_or_404(Items, pk=item_id)
    variants = item.itemvariants.all()

    if request.method == 'POST':
        new_name = request.POST.get('name')
        variant_names = request.POST.getlist('variant_name[]')
        variant_prices = request.POST.getlist('variant_price[]')

        # Check for duplicate item name (exclude current item)
        if Items.objects.filter(name=new_name).exclude(item_id=item.item_id).exists():
            return render(request, 'menu/edit-item.html', {
                'item': item,
                'variants': variants,
                'message': "Another item with this name already exists."
            })

        item.name = new_name
        item.save()

        # Remove existing variants and recreate
        item.itemvariants.all().delete()
        for name, price in zip(variant_names, variant_prices):
            ItemVariants.objects.create(item=item, sku=name, price=price)

        return redirect('view_items')  # or any other success URL

    return render(request, 'menu/edit-items.html', {
        'item': item,
        'variants': variants,
    })
