from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Items, ItemVariants

def create_item(request):
    import os
    from django.conf import settings
    images_dir = os.path.join(settings.MEDIA_ROOT, 'item_images')
    available_images = []
    if os.path.exists(images_dir):
        available_images = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]

    if request.method == 'POST':
        item_name = request.POST.get('name')
        item_type = request.POST.get('type')
        item_description = request.POST.get('description')
        variant_names = request.POST.getlist('variant_name[]')
        variant_prices = request.POST.getlist('variant_price[]')
        image_file = request.FILES.get('image')

        if Items.objects.filter(name=item_name).exists() is True:
            return render(request, 'menu/create-items.html', {'message': "Item with this name already exists.", 'available_images': available_images})

        # Handle image upload
        image_field = None
        if image_file:
            image_path = f"item_images/{image_file.name}"
            full_path = os.path.join(settings.MEDIA_ROOT, image_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            image_field = image_path

        # Create the item
        item = Items.objects.create(
            name=item_name,
            image=image_field,
            type=item_type,
            description=item_description,
            is_active=True
        )

        is_single_default_variant = (
            len(variant_names) == 1 and variant_names[0].lower() == 'default'
        )
        has_single_price = len(variant_prices) == 1

        if item_name and is_single_default_variant and has_single_price:
            # If no variants provided, create a default variant
            ItemVariants.objects.create(item=item, sku=item_name, price=variant_prices[0])
        # Create each variant
        else:
            for name, price in zip(variant_names, variant_prices):
                ItemVariants.objects.create(item=item, sku=name, price=price)

        # Log activity for item creation
        try:
            from activitylog.utils import log_activity
            log_activity(request.user, 'item_creation', item.pk, 'created')
        except Exception as e:
            print(f"[ERROR] Activity logging failed: {e}")

    from django.conf import settings as djsettings
    return render(request, 'menu/create-items.html', {
        'available_images': available_images,
        'MEDIA_URL': getattr(djsettings, 'MEDIA_URL', '/media/')
    })

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
        new_type = request.POST.get('type')
        new_description = request.POST.get('description')
        is_active = True if request.POST.get('is_active') == '1' else False
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
        item.type = new_type
        item.description = new_description
        item.is_active = is_active
        item.save()

        # Remove existing variants and recreate
        item.itemvariants.all().delete()
        for name, price in zip(variant_names, variant_prices):
            ItemVariants.objects.create(item=item, sku=name, price=price)

        # Log activity for item edit
        try:
            from activitylog.utils import log_activity
            log_activity(request.user, 'item_edit', item.pk, 'edited')
        except Exception as e:
            print(f"[ERROR] Activity logging failed: {e}")

        return redirect('view_items')  # or any other success URL

    from django.conf import settings as djsettings
    return render(request, 'menu/edit-items.html', {
        'item': item,
        'variants': variants,
        'MEDIA_URL': getattr(djsettings, 'MEDIA_URL', '/media/')
    })
