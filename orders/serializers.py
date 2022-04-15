from rest_framework import serializers
from .models import OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_id = serializers.ReadOnlyField(source='product.id')
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'product_id', 'price_total', 'quantity']