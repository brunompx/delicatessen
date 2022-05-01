from .models import *


def order_data(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        items_count = order.get_order_items_count
        return {'items_count':items_count ,'order':order, 'items':items}