from django.db import models
from django.conf import settings  # For referencing AUTH_USER_MODEL
from menu.models import ItemVariants

# class SaleProducts(models.Model):
#     product_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100, blank=True, null=True)

#     class Meta:
#         db_table = 'products'

#     def __str__(self):
#         return self.name or f"Product {self.product_id}"


# class SalePurchase(models.Model):
#     datetime = models.DateTimeField(blank=True, null=True)
#     invoice_number = models.CharField(max_length=50, blank=True, null=True)
#     supplier_name = models.CharField(max_length=50, blank=True, null=True)
#     total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
#     display = models.BooleanField(blank=True, null=True)

#     class Meta:
#         db_table = 'purchase'

#     def __str__(self):
#         return self.invoice_number or f"Purchase {self.id}"


class Sales(models.Model):
    sale_id = models.AutoField(primary_key=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    datetime = models.DateTimeField()

    class Meta:
        db_table = 'sales'

    def __str__(self):
        return f"Sale {self.sale_id}"


class Saleitems(models.Model):
    saleitem_id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    sale = models.ForeignKey(Sales, on_delete=models.CASCADE, related_name='saleitems')
    item_variant = models.ForeignKey(ItemVariants, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'saleitems'

    def __str__(self):
        return f"Sale Item {self.saleitem_id}"
