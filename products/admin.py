from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'description', 'category', 'slug', 'active']
    search_fields = ['id', 'name', 'category', 'status']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)