import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from .models import Product, Category, Order, OrderItem
from .forms import ProductForm
from .utils import  order_data
from .serializers import OrderItemSerializer

def product_home(request):
    products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, "product_home.html", context)

def product_detail_view(request, id=None):
    product_obj = None
    if id is not None:
        product_obj = Product.objects.get(id=id)
    context = {
        "product": product_obj,
    }
    return render(request, "product_detail.html", context)

def product_create_view(request, id=None):
    form = ProductForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        product_obj = form.save()
        context['form'] = ProductForm()
        return redirect(product_obj.get_absolute_url())
    return render(request, "product_create.html")
    
def order_menu_view(request):
    data = order_data(request)
    order = data['order']           #TODO: Usarlo en esta pantalla, donde?? como??
    items = data['items']           #TODO: Usarlo en esta pantalla, donde?? como??
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
    return render(request, 'order_menu.html', context)

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

    items = order.orderitem_set.all()
    serielizer = OrderItemSerializer(items, many=True)
    return JsonResponse(serielizer.data, safe=False, status=200, content_type="application/json")  #TODO: devolver los datos de la orden para mostrar en esa pantalla
