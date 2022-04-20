from django.contrib import admin
from django.urls import path, include
from orders.views import (
    order_menu_view,
    order_update_item_view,
    order_item_list,
    order_checkout_view,
    OrderList
)

urlpatterns = [

    path('order_menu/', order_menu_view, name='order_menu'),
    path('order_checkout/', order_checkout_view, name='order_checkout'),

    path('order_update_item/', order_update_item_view, name='order_update_item'),
    path('order_item_list/', order_item_list, name='order_item_list'),

    path('orders', OrderList.as_view(), name='orders'),
]