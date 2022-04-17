from datetime import timezone
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product
import random

class Order(models.Model):
    pending = 'Pending'
    completed = 'Completed'
    STATUS = (
        (pending,pending),
        (completed,completed),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True, default=random.randint(200_000, 400_000))
    # slug = models.SlugField(max_length=100, unique=True, default=random.randint(200_000, 400_000))
    comment = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length = 100, choices = STATUS)
    payment_status = models.CharField(max_length = 100, choices = STATUS)
    delivery_status = models.CharField(max_length = 100, choices = STATUS)
    complete = models.BooleanField(default = False)
    paid = models.BooleanField(default = False)
    delivered = models.BooleanField(default = False)
    if_cancelled = models.BooleanField(default = False)
    price = models.FloatField(null=True, blank=True)

    def confirmOrder(self):
        self.order_timestamp = timezone.localtime().__str__()[:19]
        self.payment_status = self.completed
        self.save()

    def confirmDelivery(self):
        self.delivery_timestamp = timezone.localtime().__str__()[:19]
        self.delivery_status = self.completed
        self.save()
    
    def __str__(self):
        return self.name
    
    def get_order_items_count(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'id': self.id})
        
class OrderItem(models.Model):
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price_individual = models.FloatField(default=0)
    price_total = models.FloatField(default=0)
