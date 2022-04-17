from django.contrib import admin
from django.urls import path, include
from orders.views import (
    order_menu_view,
    order_update_item_view
)

urlpatterns = [
    # path('', orders_home, name='orders_home'),
    # path('product/', product_home, name='product_home'),
    # path('product/create/', product_create_view, name='product_create'),
    # path('product/<int:id>/', product_detail_view, name='product_detail'),

    path('order_menu/', order_menu_view, name='order_menu'),
    path('order_update_item/', order_update_item_view, name='order_update_item'),
]