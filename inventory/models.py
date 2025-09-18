from django.db import models

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