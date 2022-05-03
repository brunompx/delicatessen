from django.contrib import admin
from django.urls import path, include
from .views import (
    order_new_view,
    order_update_item_view,
    order_item_list,
    order_checkout_view,
    OrderList,
    DeleteOrder,
    order_update_paid_view,
    order_update_delivered_view,
    order_update_view,
    order_update_cancel_view,
    print_pdf_kitchen_view,
    print_pdf_client_view
)

urlpatterns = [

    path('order_new/', order_new_view, name='order_new'),
    path('order_checkout/', order_checkout_view, name='order_checkout'),

    path('order_update_item/', order_update_item_view, name='order_update_item'),
    # path('order_update_checkbox/', order_update_checkbox_view, name='order_update_checkbox'),
    path('order_item_list/', order_item_list, name='order_item_list'),
    path('order_update_paid/<int:id>/', order_update_paid_view, name='order_update_paid'),
    path('order_update_delivered/<int:id>/', order_update_delivered_view, name='order_update_delivered'),
    path('order-update/<int:id>/', order_update_view, name='order-update'),
    path('order-update-cancel/<int:id>/', order_update_cancel_view, name='order-update-cancel'),
    path('print_pdf_kitchen/<int:id>/', print_pdf_kitchen_view, name='print_pdf_kitchen'),
    path('print_pdf_client/<int:id>/', print_pdf_client_view, name='print_pdf_client'),

    path('', OrderList.as_view(), name='index'),
    path('orders', OrderList.as_view(), name='orders'),
    path('order_delete/<int:pk>/', DeleteOrder.as_view(), name='order_delete'),
    # path('order-update/<int:pk>/', OrderUpdate.as_view(), name='order-update'),
    
]