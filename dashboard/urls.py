from django.urls import path, include
from .views import (
    sales_by_category_view,
    sales_by_product_view,
    sales_by_order_view
)

urlpatterns = [
    path('category_dash/', sales_by_category_view, name='category_dash'),
    path('product_dash/', sales_by_product_view, name='product_dash'),
    path('order_dash/', sales_by_order_view, name='order_dash'),
]