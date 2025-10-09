from django.db import models
from django.conf import settings

class Ingredient(models.Model):
    class Meta:
        db_table = 'ingredients'
    name = models.CharField(max_length=45)
    quantity = models.IntegerField()
    unit_of_measure = models.CharField(max_length=25)
    expiry_date = models.DateField()
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


#NEW STUFF

class RawItem(models.Model):
    class Meta:
        db_table = 'raw_items'
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_of_measurement = models.CharField(max_length=25, blank=True, null=True)
    description = models.TextField()
    display = models.BooleanField(default=True)
    

    def __str__(self):
        return self.name

class Purchase(models.Model):
    class Meta:
        db_table = 'purchase'
    id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField()
    invoice_number = models.CharField(max_length=50)
    supplier_name = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    display = models.BooleanField(default=True)

class StoreroomItem(models.Model):
    class Meta:
        db_table = 'storeroom_items'
    id = models.AutoField(primary_key=True)
    po_id = models.IntegerField()
    raw_item_id = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    display = models.BooleanField(default=True)

class Transfer(models.Model):
    class Meta:
        db_table = 'transfer'
    id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField()
    reason = models.CharField(max_length=50)
    from django.conf import settings

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    display = models.BooleanField(default=True)

class TransferItem(models.Model):
    class Meta:
        db_table = 'transfer_items'
    id = models.AutoField(primary_key=True)
    transfer_id = models.IntegerField()
    raw_item_id = models.IntegerField()
    quantity = models.DecimalField(max_digits=50, decimal_places=2)
    display = models.BooleanField(default=True)


class Storeroom(models.Model):
    class Meta:
        db_table = 'storeroom'
    id = models.AutoField(primary_key=True)
    raw_item = models.ForeignKey(RawItem, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    display = models.BooleanField(default=True)