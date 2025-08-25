from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    #I ADDED A USERNAME
    username = models.CharField(max_length=150, blank=True)
    pass

    def __str__(self):
        return self.email