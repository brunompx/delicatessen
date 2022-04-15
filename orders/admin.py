from django.contrib import admin
from .models import Product, Category, Order, OrderItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'category', 'status']
    search_fields = ['id', 'name', 'category', 'status']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'comment', 'complete', 'paid', 'delivered']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'quantity', 'product', 'order', 'price_individual', 'price_total']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)