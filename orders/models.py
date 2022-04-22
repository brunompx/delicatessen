from datetime import datetime, timedelta
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from products.models import Product
import random

# class LastCompletedManager(models.Manager):
#     def get_queryset(self):
#         current_time = datetime.now()
#         past_time = current_time - timedelta(hours=24)
#         return super().get_queryset().filter(completed=True, timestamp > past_time)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    comment = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default = False)
    paid = models.BooleanField(default = False)
    delivered = models.BooleanField(default = False)
    if_cancelled = models.BooleanField(default = False)
    price = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username + datetime.now().strftime("%Y%m%d%H%M%S"))
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_order_items_count(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'slug': self.slug})

    @property
    def get_order_total(self):
        order_items = self.orderitem_set.all()
        if order_items.count() > 0:
            total = sum([item.price_total for item in order_items])
            return total 
        return 0.0
        
        
class OrderItem(models.Model):
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price_individual = models.FloatField(default=0)
    price_total = models.FloatField(default=0)
