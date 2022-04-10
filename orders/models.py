from datetime import timezone
from django.db import models



class Order(models.Model):
    pending = 'Pending'
    completed = 'Completed'
    STATUS = (
        (pending,pending),
        (completed,completed),
    )
    comment = models.TextField()
    order_timestamp = models.CharField(max_length=100, blank=True)
    delivery_timestamp = models.CharField(max_length=100, blank=True)
    payment_status = models.CharField(max_length = 100, choices = STATUS)
    delivery_status = models.CharField(max_length = 100, choices = STATUS)
    if_cancelled = models.BooleanField(default = False)
    price = models.IntegerField()

    def confirmOrder(self):
        self.order_timestamp = timezone.localtime().__str__()[:19]
        self.payment_status = self.completed
        self.save()

    def confirmDelivery(self):
        self.delivery_timestamp = timezone.localtime().__str__()[:19]
        self.delivery_status = self.completed
        self.save()
    
    def __str__(self):
        return self.customer.__str__()

class Category(models.Model):
    name = models.CharField(max_length=250)

class Food(models.Model):
    disabled = 'Disabled'
    enabled = 'Enabled'
    STATUS = (
        (disabled, disabled),
        (enabled, enabled),
    )
    name = models.CharField(max_length=250)
    description = models.TextField()
    recipe = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS)
    price = models.FloatField()
    num_order = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    quantity = models.IntegerField(default=1)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price_individual = models.FloatField()
    price = models.FloatField()
