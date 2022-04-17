from django.db import models
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Product(models.Model):
    disabled = 'Disabled'
    enabled = 'Enabled'
    STATUS = (
        (disabled, disabled),
        (enabled, enabled),
    )
    name = models.CharField(max_length=250, unique=True)
    # slug = models.SlugField(max_length=100, unique=True, default=random.randint(200_000, 400_000))
    description = models.TextField(null=True, blank=True)
    # recipe = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS)
    price = models.FloatField(null=True, blank=True)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'id': self.id})