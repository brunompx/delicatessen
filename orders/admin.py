from django.contrib import admin
from .models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'comment', 'complete', 'paid', 'delivered', 'slug']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'quantity', 'product', 'order', 'price_individual', 'price_total']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)