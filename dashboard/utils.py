from datetime import datetime, timedelta
from products.models import Product, Category
from orders.models import Order, OrderItem


# Categrories data for PIE chart
def categories_amount_by_date_range(query_set):
    # query_set = OrderItem.objects.filter(order__checkout_date__range=(from_datetime, to_datetime))
    map_by_category = {}
    for order_item in query_set:
        category_name = order_item.product.category.name
        price_total = int(order_item.price_total)
        if category_name in map_by_category:
            map_by_category[category_name] += price_total
        else:
            map_by_category[category_name] = price_total
    return map_to_chartmap(map_by_category)


# Categrory data for LINE chart
def category_count_by_date_range(query_set, from_datetime, to_datetime):

    days_count = get_dates_diff(from_datetime, to_datetime)
    data_map = {}
    increment_date = from_datetime

    if days_count < 3:
        while not same_hour(increment_date, (to_datetime + timedelta(hours=1))):
            sales_count = 0
            for item in query_set:
                if same_hour(increment_date, item.order.checkout_date):
                    sales_count += item.quantity
            data_map[increment_date.strftime("%d-%H")] = sales_count
            increment_date = increment_date + timedelta(hours=1)

    if days_count >= 3 and days_count < 20:
        while not same_day(increment_date, (to_datetime + timedelta(days=1))):
            sales_count = 0
            for item in query_set:
                if same_day(increment_date, item.order.checkout_date):
                    sales_count += item.quantity
            data_map[increment_date.strftime("%m-%d")] = sales_count
            increment_date = increment_date + timedelta(days=1)

    if days_count >= 20 and days_count < 80:
        while not same_week(increment_date, (to_datetime + timedelta(days=7))):
            sales_count = 0
            for item in query_set:
                if same_week(increment_date, item.order.checkout_date):
                    sales_count += item.quantity
            data_map[increment_date.strftime("%m-%d")] = sales_count #TODO como almacenar semana
            increment_date = increment_date + timedelta(days=7)

    if days_count >= 80:
        while not same_month(increment_date, (to_datetime + timedelta(days=30))):
            sales_count = 0
            for item in query_set:
                if same_month(increment_date, item.order.checkout_date):
                    sales_count += item.quantity
            data_map[increment_date.strftime("%Y-%m")] = sales_count
            increment_date = increment_date + timedelta(days=30)

    print(data_map)
    print('hour', same_hour(from_datetime, to_datetime))
    print('day', same_day(from_datetime, to_datetime))
    print('week', same_week(from_datetime, to_datetime))
    print('month', same_month(from_datetime, to_datetime))
    return map_to_chartmap(data_map)

def map_to_chartmap(data_map):
    labels = []
    data = []
    for k, v in data_map.items():
        labels.append(k)
        data.append(v)
    map_data = {'data':data, 'labels':labels}
    return map_data

def get_dates_diff(from_datetime, to_datetime):
    days_count = (to_datetime - from_datetime).days
    print('days count', days_count)
    return days_count

def same_hour(datetime_a, datetime_b):
    return datetime_a.date() == datetime_b.date() and datetime_a.hour == datetime_b.hour

def same_day(datetime_a, datetime_b):
    return datetime_a.date() == datetime_b.date()

def same_week(datetime_a, datetime_b):
    return datetime_a.year == datetime_b.year and datetime_a.isocalendar()[1] == datetime_b.isocalendar()[1]

def same_month(datetime_a, datetime_b):
    return datetime_a.year == datetime_b.year and datetime_a.month == datetime_b.month


# Products data for PIE chart
def products_amount_by_cat_date_range(category_name, from_datetime, to_datetime):
    qs = OrderItem.objects.filter(product__category=category_name, order__checkout_date__range=(from_datetime, to_datetime))
    map_by_products = {}
    for order_item in qs:
        product_name = order_item.product.name
        price_total = int(order_item.price_total)
        if category_name in map_by_products:
            map_by_products[product_name] += price_total
        else:
            map_by_products[product_name] = price_total
    labels = []
    data = []
    for k, v in map_by_products.items():
        labels.append(k)
        data.append(v)
    map_data = {'data':data, 'labels':labels}
    return map_data
