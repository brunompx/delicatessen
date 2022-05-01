import json
from django.shortcuts import render
from .forms import FromToForm, SalesByCategoryForm, SalesByProductForm, SalesByOrderForm
from .utils import (
    categories_amount_by_date_range, 
    products_amount_by_cat_date_range, 
    category_count_by_date_range
)
from orders.models import OrderItem, Order



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
            pie_map = categories_amount_by_date_range(qs)
            context['pie_data'] = json.dumps(pie_map['data'])
            context['pie_labels'] = json.dumps(pie_map['labels'])

            # data and labels for LINE chart
            line_map = category_count_by_date_range(qs_category, from_datetime, to_datetime)
            context['line_data'] = json.dumps(line_map['data'])
            context['line_labels'] = json.dumps(line_map['labels'])

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

            # data and labels for PIE chart
            if qs:
                category_name = qs[0].product.category
                pie_data_map = products_amount_by_cat_date_range(category_name, from_datetime, to_datetime)
                context['pie_data'] = json.dumps(pie_data_map['data'])
                context['pie_labels'] = json.dumps(pie_data_map['labels'])

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