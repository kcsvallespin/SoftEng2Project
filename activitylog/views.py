from django.shortcuts import get_object_or_404
def log_detail(request, log_id):
	log = get_object_or_404(Log, pk=log_id)
	transfer_items = None
	raw_item_detail = None
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
	return render(request, 'activitylog/log_detail.html', {'log': log, 'transfer_items': transfer_items, 'raw_item_detail': raw_item_detail})
from django.shortcuts import render

# Create your views here.
from .models import Log

def view_logs(request):
	logs = Log.objects.select_related('user').order_by('-date_time')[:200]
	return render(request, 'activitylog/viewlogs.html', {'logs': logs})
