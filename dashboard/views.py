from django.shortcuts import render
from .forms import FromToForm, SalesByCategoryForm, SalesByProductForm, SalesByOrderForm
from orders.models import OrderItem, Order



def sales_by_category_view(request):
    context = {}
    if request.method == 'POST':
        form = SalesByCategoryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            from_datetime = form.get_from_datetime()
            to_datetime = form.get_to_datetime()
            qs = OrderItem.objects.filter(product__category=category, order__checkout_date__range=(from_datetime, to_datetime))
            qs = qs.order_by('-order__checkout_date')
            context['order_items'] = qs
    else:
        form = SalesByCategoryForm()
    context['form'] = form
    return render(request, 'category_dash.html', context)

def sales_by_product_view(request):
    context = {}
    if request.method == 'POST':
        form = SalesByProductForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            from_datetime = form.get_from_datetime()
            to_datetime = form.get_to_datetime()
            qs = OrderItem.objects.filter(product=product, order__checkout_date__range=(from_datetime, to_datetime))
            qs = qs.order_by('-order__checkout_date')
            context['order_items'] = qs
    else:
        form = SalesByProductForm()
    context['form'] = form
    return render(request, 'product_dash.html', context)

def sales_by_order_view(request):
    context = {}
    if request.method == 'POST':
        form = FromToForm(request.POST)
        if form.is_valid():
            from_datetime = form.get_from_datetime()
            to_datetime = form.get_to_datetime()
            qs = Order.objects.filter(complete=True, checkout_date__range=(from_datetime, to_datetime))
            qs = qs.order_by('-checkout_date')
            context['orders'] = qs
    else:
        form = FromToForm()
    context['form'] = form
    return render(request, 'order_dash.html', context)