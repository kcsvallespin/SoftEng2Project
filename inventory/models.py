from django.db import models

class Supplier(models.Model):
    class Meta:
        db_table = 'suppliers'
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    supplier_email = models.CharField(max_length=100)
    supplier_phone = models.CharField(max_length=20)
    address = models.TextField()
    website = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.supplier_name

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
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.name