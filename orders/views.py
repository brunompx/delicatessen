import json
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order, OrderItem
from .utils import  order_data
from .serializers import OrderItemSerializer
from .forms import OrderForm, OrderUpdateForm
from products.models import Product, Category


# Function Views ----------------------------------------------------------------

def order_new_view(request):
    data = order_data(request)
    order = data['order']
    items = data['items']
    items_count = data['items_count']
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products':products, 
        'items_count':items_count, 
        'categories':categories,
        'items':items, 
        'order':order
        }
    return render(request, 'order_new.html', context)

def order_update_item_view(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    user = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user=user, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.price_individual = product.price
    orderItem.price_total = product.price * orderItem.quantity
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

def order_checkout_view(request):
    data = order_data(request)
    order = data['order']
    items = data['items']
    items_count = data['items_count']
    form = OrderForm(request.POST or None, instance=order)
    context = {
        'items': items,
        'order': order,
        'items_count': items_count,
        'form': form
        }
    if form.is_valid():
        order_object = form.save()
        order_object.complete = True
        order_object.checkout_date = datetime.today()
        order_object.price = order_object.get_order_total
        order_object.save()
        for item in order_object.orderitem_set.all():
            product = Product.objects.get(id=item.product.id)
            if product.stock > item.quantity:
                product.stock -= item.quantity
            else:
                product.stock = 0
            product.save()
        return redirect('orders')
    return render(request, 'order_checkout.html', context)

def order_update_paid_view(request, id=None):
    if id is not None:
        order = Order.objects.get(id=id)
        order.paid = not order.paid
        order.save()
    return redirect('orders')

def order_update_delivered_view(request, id=None):
    if id is not None:
        order = Order.objects.get(id=id)
        order.delivered = not order.delivered
        order.save()
    return redirect('orders')

def order_update_view(request, id=None):
    user = request.user
    if id is not None:
        Order.objects.filter(user=user, complete=False).delete()
        order = Order.objects.get(user=user, id=id)
        order.complete = False
        order.save()
    return redirect('order_new')

def order_update_cancel_view(request, id=None):
    user = request.user
    if id is not None:
        order = Order.objects.get(user=user, id=id)
        order.complete = True
        order.save()
    return redirect('orders')


# API Views ----------------------------------------------------------------

@api_view(['GET'])
def order_item_list(request):
    user = request.user
    order, created = Order.objects.get_or_create(user=user, complete=False)
    items = order.orderitem_set.all()
    serializer = OrderItemSerializer(items, many=True)
    return Response(serializer.data)


# Class Views ----------------------------------------------------------------

class OrderList(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        time_filter = datetime.today() - timedelta(hours=200)
        queryset = Order.objects.filter(complete=True, checkout_date__gt=time_filter)
        queryset = queryset.order_by('-checkout_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = OrderItem.objects.all()
        return context

class DeleteOrder(LoginRequiredMixin, DeleteView):
    model = Order
    context_object_name = 'order'
    success_url = reverse_lazy('orders')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderUpdateForm
    success_url = reverse_lazy('orders')