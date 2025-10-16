from django.db import models
from django.utils import timezone

# class AccountsCustomuser(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.BooleanField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.BooleanField()
#     is_active = models.BooleanField()
#     date_joined = models.DateTimeField()

#     class Meta:
#         db_table = 'accounts_customuser'

#     def __str__(self):
#         return self.username


class Items(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'items'

    def __str__(self):
        return self.name


class ItemVariants(models.Model):
    variant_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='itemvariants')
    sku = models.CharField(unique=True, max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_default = models.BooleanField(blank=True, null=True)
    inventory_enabled = models.BooleanField(blank=True, null=True)
    current_stock = models.IntegerField(blank=True, null=True)
    reorder_threshold = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'item_variants'

    def __str__(self):
        return self.sku or f"Variant {self.variant_id}"


# class Products(models.Model):
#     product_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100, blank=True, null=True)

#     class Meta:
#         db_table = 'products'

#     def __str__(self):
#         return self.name or f"Product {self.product_id}"
