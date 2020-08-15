from django.shortcuts import render, reverse
from django.http import JsonResponse
from .models import Item
from accounts.models import Farmer
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from images.models import Image
import random

# Create your views here.
@login_required(login_url='/accounts/login')
def home(request):
    c1 = Q(state = request.user.profile.state)
    c2 = Q(city = request.user.profile.city)
    farmers = Farmer.objects.filter(c1&c2)
    items_ = []
    for farmer in farmers:
        for item in farmer.items.all():
            if(item.quantity > 0):
                items_.append(item)
            else:
                pass

    items_ = sorted(items_, key=lambda x: random.randint(0,len(items_)))
    items = []

    if len(request.GET) == 0 or request.GET['item'] == '':
        items = items_
    else:
        item_name = request.GET['item']
        for item in items_:
            if item.name == item_name:
                items.append(item)
        items = sorted(items, key=lambda x:x.price)


    context = {
        'items':items
    }
    #print(reverse('add_item_to_database'))
    return render(request, 'shop/home.html', context)

@login_required(login_url='/accounts/login')
def detail(request, pk):
    item = Item.objects.get(pk=pk)

    context = {
        'item':item
    }
    return render(request, 'shop/detail.html', context)

@csrf_exempt
def sms(request):
    data = request.body.decode('utf-8')
    a = data.split(',')
    print(a)
    d = list(map(lambda x: x.split(":"), a))
    print(d)
    data = dict([])
    for i in d:
        data[i[0]] = i[1]
    print(data)

    farmernumber = data['phonenumber']
    farmer = Farmer.objects.get(phonenumber=farmernumber)

    item_image = Image.objects.get(tag=data['name']).image
    item = Item(name=data['name'], price=data['price'], image=item_image, quantity=data['quantity'], farmer=farmer)
    item.save()

    return JsonResponse({'ok':True})
