from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *

def store(request):
     products = Product.objects.all()
     context = {'products':products}
     return render(request, 'store/store.html', context)

def cart(request):

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
     else:
          items = []
          order = {'get_cart_total':0, 'get_cart_items':0}

     context = {'items':items, 'order':order}
     return render(request, 'store/cart.html', context)

def checkout(request):
     if request.user.is_authenticated:
           customer = request.user.customer
           order, created = Order.objects.get_or_create(customer=customer, complete=False)
           items = order.orderitem_set.all()
     else:
          order = {'get_cart_total':0, 'get_cart_items':0}
          items = []


     context = {'items':items, 'order':order}
     return render(request, 'store/checkout.html', context)


def updateItem(request):
     data = json.loads(request.data)
     productID = data['productID']
     action = data['action']

     print('Action:', action)
     print('productID:', productID)

     customer = request.user.customer
     product = product.objects.get(id=productID)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)

     OrderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

     if action == 'add':
          OrderItem.quantity = (OrderItem.quantity + 1)
     elif action == 'remove':
          OrderItem.quantity = (OrderItem.quantity - 1)

     OrderItem.save()

     if OrderItem.quantity <= 0:
          OrderItem.delete()

     return JsonResponse('Item was added', safe=False)