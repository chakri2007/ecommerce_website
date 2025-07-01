from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    contact = models.CharField(max_length=100, unique=True)
    ACCOUNT_CHOICES = [('buyer', 'Buyer'), ('seller', 'Seller')]
    account_type = models.CharField(max_length=10, choices=ACCOUNT_CHOICES)

    def __str__(self):
        return self.username
