from django.shortcuts import get_object_or_404
def log_detail(request, log_id):
	purchase_detail = None
	purchase_items = None
	sale_detail = None
	sale_items = None
	log = get_object_or_404(Log, pk=log_id)
	transfer_items = None
	raw_item_detail = None
	item_detail = None
	item_variants = None
	if log.transaction_type == 'TRANSFER':
		from inventory.models import TransferItem, RawItem
		transfer_items = TransferItem.objects.filter(transfer_id=log.reference_id)
		item_map = {item.id: item.name for item in RawItem.objects.all()}
		for ti in transfer_items:
			ti.item_name = item_map.get(ti.raw_item_id, f"ID {ti.raw_item_id}")
	elif log.transaction_type == 'RAW_ITEM':
		from inventory.models import RawItem
		try:
			raw_item_detail = RawItem.objects.get(id=log.reference_id)
		except RawItem.DoesNotExist:
			raw_item_detail = None
	elif log.transaction_type in ['sale_creation', 'sale_edit']:
		from sales.models import Sales, Saleitems
		try:
			sale_detail = Sales.objects.get(pk=log.reference_id)
			sale_items = Saleitems.objects.filter(sale=sale_detail).select_related('item_variant__item')
		except Sales.DoesNotExist:
			sale_detail = None
			sale_items = None
	elif log.transaction_type == 'PURCHASE':
		from inventory.models import Purchase, StoreroomItem, RawItem
		try:
			purchase_detail = Purchase.objects.get(pk=log.reference_id)
			purchase_items = StoreroomItem.objects.filter(po_id=purchase_detail.id)
			raw_item_map = {ri.id: ri.name for ri in RawItem.objects.all()}
			for pi in purchase_items:
				pi.raw_item_name = raw_item_map.get(pi.raw_item_id, f"ID {pi.raw_item_id}")
		except Purchase.DoesNotExist:
			purchase_detail = None
			purchase_items = None
	elif log.transaction_type in ['item_creation', 'item_edit']:
		from menu.models import Items, ItemVariants
		try:
			item_detail = Items.objects.get(pk=log.reference_id)
			item_variants = ItemVariants.objects.filter(item=item_detail)
		except Items.DoesNotExist:
			item_detail = None
			item_variants = None
	from django.conf import settings
	return render(request, 'activitylog/log_detail.html', {
		'log': log,
		'transfer_items': transfer_items,
		'raw_item_detail': raw_item_detail,
		'item_detail': item_detail,
		'item_variants': item_variants,
		'sale_detail': sale_detail,
		'sale_items': sale_items,
		'purchase_detail': purchase_detail,
		'purchase_items': purchase_items,
		'MEDIA_URL': getattr(settings, 'MEDIA_URL', '/media/')
	})
from django.shortcuts import render

# Create your views here.
from .models import Log

def view_logs(request):
	logs = Log.objects.select_related('user').order_by('-date_time')[:200]
	return render(request, 'activitylog/viewlogs.html', {'logs': logs})
