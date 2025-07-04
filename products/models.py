from django.db import models
from django.conf import settings

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=1)
    image_url = models.URLField(blank=True, null=True)  # Replaces ImageField
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
