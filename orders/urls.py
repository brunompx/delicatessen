from django.contrib import admin
from django.urls import path, include
from .views import (
    order_new_view,
    order_update_item_view,
    order_item_list,
    order_checkout_view,
    OrderList,
    order_update_checkbox_view
)

urlpatterns = [

    path('order_new/', order_new_view, name='order_new'),
    path('order_checkout/', order_checkout_view, name='order_checkout'),

    path('order_update_item/', order_update_item_view, name='order_update_item'),
    path('order_update_checkbox/', order_update_checkbox_view, name='order_update_checkbox'),
    path('order_item_list/', order_item_list, name='order_item_list'),

    path('orders', OrderList.as_view(), name='orders'),
]