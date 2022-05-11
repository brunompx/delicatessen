import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import FromToForm, SalesByCategoryForm, SalesByProductForm, SalesByOrderForm
from .utils import (
    categories_data_pie_chart, 
    products_data_pie_chart, 
    orderitem_data_line_chart,
    orders_data_line_chart
)
from orders.models import OrderItem, Order


@login_required
def sales_by_category_view(request):
    context = {}
    if request.method == 'POST':
        form = SalesByCategoryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            from_datetime = form.get_from_datetime()
            to_datetime = form.get_to_datetime()

            # data for TABLE
            qs = OrderItem.objects.filter(order__checkout_date__range=(from_datetime, to_datetime))
            qs_category = qs.filter(product__category=category).order_by('-order__checkout_date')
            context['order_items'] = qs_category

            # data for CARDS
            count = sum(item.quantity for item in qs_category)
            amount = sum(item.price_total for item in qs_category)
            context['count'] = count
            context['amount'] = amount

            # data and labels for PIE chart
            pie_map = categories_data_pie_chart(qs)
            context['pie_data'] = json.dumps(pie_map['data'])
            context['pie_labels'] = json.dumps(pie_map['labels'])

            # data and labels for LINE chart
            line_map = orderitem_data_line_chart(qs_category, from_datetime, to_datetime)
            context['line_data'] = json.dumps(line_map['data'])
            context['line_labels'] = json.dumps(line_map['labels'])

    else:
        form = SalesByCategoryForm()
    context['form'] = form
    return render(request, 'category_dash.html', context)


@login_required
def sales_by_product_view(request):
    context = {}
    if request.method == 'POST':
        form = SalesByProductForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            from_datetime = form.get_from_datetime()
            to_datetime = form.get_to_datetime()

            # data for TABLE
            qs = OrderItem.objects.filter(order__checkout_date__range=(from_datetime, to_datetime))
            qs_product = qs.filter(product=product).order_by('-order__checkout_date')
            qs_category = qs.filter(product__category=qs_product[0].product.category).order_by('-order__checkout_date')
            context['order_items'] = qs_product

            # data for CARDS
            count = sum(item.quantity for item in qs_product)
            amount = sum(item.price_total for item in qs_product)
            context['count'] = count
            context['amount'] = amount

            # data and labels for PIE chart
            pie_map = products_data_pie_chart(qs_category)
            context['pie_data'] = json.dumps(pie_map['data'])
            context['pie_labels'] = json.dumps(pie_map['labels'])

            # data and labels for LINE chart
            line_map = orderitem_data_line_chart(qs_product, from_datetime, to_datetime)
            context['line_data'] = json.dumps(line_map['data'])
            context['line_labels'] = json.dumps(line_map['labels'])

    else:
        form = SalesByProductForm()
    context['form'] = form
    return render(request, 'product_dash.html', context)


@login_required
def sales_by_order_view(request):
    context = {}
    if request.method == 'POST':
        form = FromToForm(request.POST)
        if form.is_valid():
            from_datetime = form.get_from_datetime()
            to_datetime = form.get_to_datetime()

            # data for TABLE
            qs = Order.objects.filter(complete=True, checkout_date__range=(from_datetime, to_datetime))
            qs = qs.order_by('-checkout_date')
            context['orders'] = qs

            # data for CARDS
            count = len(qs)
            amount = sum(order.price for order in qs)
            context['count'] = count
            context['amount'] = amount

            # data and labels for LINE chart
            line_map = orders_data_line_chart(qs, from_datetime, to_datetime)
            print(line_map)
            context['line_data'] = json.dumps(line_map['data'])
            context['line_labels'] = json.dumps(line_map['labels'])

    else:
        form = FromToForm()
    context['form'] = form
    return render(request, 'order_dash.html', context)