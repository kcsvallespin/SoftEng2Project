from django.db import models
from accounts.models import CustomUser

class Log(models.Model):
	id = models.AutoField(primary_key=True)
	transaction_type = models.CharField(max_length=25)
	reference_id = models.IntegerField()
	action = models.CharField(max_length=50)
	date_time = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.transaction_type} - {self.action} by {self.user}" 
from django.db import models

# Create your models here.
