from django.shortcuts import render, reverse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from shop.models import Item
from .models import Cart, CartItem, Order
import requests
from payments import Checksum
from django.contrib.auth.models import User

from django.core.mail import send_mail
import json


# Create your views here.

@login_required(login_url='/accounts/login')
def add_to_cart(request):
    pk = request.POST['pk']
    quantity = request.POST['quantity']
    item = Item.objects.get(pk=pk)
    cart = request.user.cart

    cartitem = CartItem(item_id=pk,cart=cart, price=item.price, image=item.image, farmer=item.farmer, name=item.name, quantity=int(quantity))
    cart.amount += cartitem.price*float(quantity)

    item.quantity -= int(quantity)
    item.save()
    cartitem.save()
    cart.save()

    return HttpResponseRedirect(reverse('detail', args=(pk,)))


@login_required(login_url='/accounts/login')
def show_cart(request):
    user = request.user
    cart = user.cart
    items = [x for x in cart.items.all() if x.status == False]
    amount = cart.amount
    context = {
    'items':items,
    'amount': amount,
    'shipping': amount*0.4,
    'tax': amount*0.2,
    'total':amount*(1.6)
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url='/accounts/login')
def  delete_from_cart(request, pk):
    item = CartItem.objects.get(pk=pk)
    item_ = Item.objects.get(id=item.item_id)
    item_.quantity += item.quantity
    cart = request.user.cart
    cart.amount -= item.price*item.quantity
    cart.save()
    item_.save()
    item.delete()
    return HttpResponseRedirect(reverse('showcart'))

def pay(request, pk):
    cartitem = CartItem.objects.get(pk=pk)
    farmer = cartitem.farmer
    customer = request.user
    cartitem.status = True
    order = Order(user=request.user, item=cartitem, name=cartitem.name, price=cartitem.price, quantity=cartitem.quantity, farmer=cartitem.farmer, location=f"{farmer.state} {farmer.city}")
    order.save()
    cartitem.save()
    params = {
        "MID": f"{farmer.mid}",
        "ORDER_ID": f"{order.e}",
        "CUST_ID": f"qqwwee{customer.pk}",
        "TXN_AMOUNT": f"{cartitem.price*cartitem.quantity}",
        "CHANNEL_ID": "WEB",
        "INDUSTRY_TYPE_ID": "Retail",
        "WEBSITE": "WEBSTAGING",
        "CALLBACK_URL":'https://092ffd4b.ngrok.io/cart/handelrequest'
    }
    params['CHECKSUMHASH'] = Checksum.generate_checksum(params, f'{farmer.mkey}')
    return render(request, 'payments/paytm.html', {'params':params})


@csrf_exempt
def handelrequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    if response_dict['STATUS'] != 'TXN_FAILURE':
        d = response_dict['ORDERID']
        order = Order.objects.get(e=str(d))
        cartitem = order.item
        cart = cartitem.cart
        cart.amount -= cartitem.price*cartitem.quantity
        cart.save()
        del response_dict['CHECKSUMHASH']
        del response_dict['MID']
        del response_dict['RESPCODE']
    return render(request, 'payments/status.html', {'respons_dict':response_dict})

@login_required(login_url='/accounts/login')
def orders(request):
    user = request.user
    orders = [order for order in Order.objects.all() if order.user == user and order.received==False]
    context = {
        'orders':orders
    }

    return render(request, 'cart/orders.html', context)

@login_required(login_url='/accounts/login')
def track_order(request, id):
    order = Order.objects.get(e=id)
    msg = f"you'r order of id {order.e} is at {order.location}"
    send_mail(
        'order tracking',
        msg,
        'rohit20001221@gmail.com',
        [request.user.email,]
    )
    return HttpResponseRedirect(reverse('orders'))

@login_required(login_url='/accounts/login')
def order_received(request, id):
    order = Order.objects.get(e=id)
    order.received = True
    order.save()
    return HttpResponseRedirect(reverse('orders'))
