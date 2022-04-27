from products.models import Product, Category
from orders.models import Order, OrderItem



def categories_amount_by_date_range(from_datetime, to_datetime):
    qs = OrderItem.objects.filter(order__checkout_date__range=(from_datetime, to_datetime))
    map_by_category = {}
    for order_item in qs:
        category_name = order_item.product.category.name
        price_total = int(order_item.price_total)
        if category_name in map_by_category:
            map_by_category[category_name] += price_total
        else:
            map_by_category[category_name] = price_total
    labels = []
    data = []
    for k, v in map_by_category.items():
        labels.append(k)
        data.append(v)
    map_data = {'data':data, 'labels':labels}
    return map_data
