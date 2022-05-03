import io
from reportlab.lib.pagesizes import A7
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from .models import *


def order_data(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        items_count = order.get_order_items_count
        return {'items_count':items_count ,'order':order, 'items':items}


def build_pdf_client(request, id):

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=A7, bottomup=0)

    order = Order.objects.get(user=request.user, id=id)

    text_o = p.beginText()
    text_o.setTextOrigin(0.5*cm, cm)
    text_o.setFont('Helvetica', 11)

    lines = []
    
    lines.append("---Angula Delivery---")
    lines.append(" ------------------------- ")
    lines.append(" --- " + order.name + " --- ")
    lines.append(" ------------------------- ")
    lines.append(" ")

    for item in order.orderitem_set.all():
        # product = Product.objects.get(user=request.user, id=item.product.id)
        lines.append(item.product.name + "  " + "x" + " " + str(item.quantity) + "  " + "$" + str(item.price_total))

    lines.append(" ")
    lines.append("TOTAL :  $ " + str(order.price))
    lines.append(" ")
    lines.append(" ------------------------- ")

    for line in lines:
        text_o.textLine(line)

    p.drawText(text_o)

    p.showPage()
    p.save()
    buffer.seek(0)

    return buffer


def build_pdf_kitchen(request, id):

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=A7, bottomup=0)

    order = Order.objects.get(user=request.user, id=id)

    text_o = p.beginText()
    text_o.setTextOrigin(0.5*cm, cm)
    text_o.setFont('Helvetica', 12)


    items_dic = {}
    for item in order.orderitem_set.all():
        if item.product.category.name in items_dic:
            items_dic[item.product.category.name].append(item.product.name + " ------ " + "x" + " " + str(item.quantity))
        else:
            category_list = []
            category_list.append(item.product.name + " ------ " + "x" + " " + str(item.quantity))
            items_dic[item.product.category.name] = category_list

    lines = []
    
    lines.append(" ------------------------- ")
    lines.append(" ------- " + order.name + " ------- ")
    lines.append(" ------------------------- ")
    lines.append(" ------- Hora: " + order.delivery_time + " ------- ")
    lines.append(" ------------------------- ")
    lines.append(" ")

    print(items_dic)

    for k, v in items_dic.items():
        lines.append(" ------- " + k.upper() + " ------- ")
        lines.append(" ")
        for line in v:
            lines.append(line)
        lines.append(" ")

    lines.append(" ")
    lines.append(" ------------------------- ")

    for line in lines:
        text_o.textLine(line)

    p.drawText(text_o)

    p.showPage()
    p.save()
    buffer.seek(0)

    return buffer