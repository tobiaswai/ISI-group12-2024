from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
import json
import datetime
from .models import *

from django.core.paginator import Paginator
from django.db.models import Q


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']
        full_name = request.POST['full_name']
        shipping_address = request.POST['shipping_address']
        
        if User.objects.filter(username=username).exists():
            msg = 'This username has already been taken. Please choose a different one.'
            return render(request, 'register.html', locals())
        
        if User.objects.filter(email=email).exists():
            msg = 'This email has already been registered. Please use a different email.'
            return render(request, 'register.html', locals())
        
        if password != password2:
            msg = 'Passwords are inconsistent'
            return render(request, 'register.html', locals())
        
        # Create User object
        user = User.objects.create_user(username=username, password=password, email=email)
        
        # Create Customer object
        Customer.objects.create(user=user, password=password, full_name=full_name, email=email, shipping_address=shipping_address)

        return redirect('login')
    
    return render(request, 'register.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            #msg = 'You have successfully logged in!'
            return redirect('store/main.html')
        else:
            #messages.error(request, 'Invalid credentials.')
            msg = 'username or password is incorrect'
            return render(request,'login.html',locals())
    return render(request, 'login.html')

def store(request):

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
          items = []
          order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}    
          cartItems = order['get_cart_items'] 

     if 'q' in request.GET:
          q = request.GET['q']
          products = Product.objects.filter(name__icontains=q, is_active=True)
     else:
          products = Product.objects.filter(is_active=True)
          
     page = Paginator(products, 6)
     page_list = request.GET.get('page')
     page = page.get_page(page_list)
     products = Product.objects.filter(is_active=True)
     context = {'products':products, 'cartItems':cartItems, 'page': page}
     return render(request, 'store/store.html', context)

def product(request, pk):
     
     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
          items = []
          order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
          cartItems = order['get_cart_items']
     
     product = Product.objects.get(id=pk)
     context = {'products':product, 'cartItems':cartItems}
     return render(request, 'store/product.html', context)

def cart(request):

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
          items = []
          order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
          cartItems = order['get_cart_items']

     products = Product.objects.all()
     context = {'products':products, 'items':items, 'order':order, 'cartItems':cartItems}
     return render(request, 'store/cart.html', context)

def checkout(request):
     if request.user.is_authenticated:
           customer = request.user.customer
           order, created = Order.objects.get_or_create(customer=customer, complete=False)
           items = order.orderitem_set.all()
           cartItems = order.get_cart_items
     else:
          items = []
          order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
          cartItems = order['get_cart_items']


     context = {'items':items, 'order':order, 'cartItems':cartItems}
     return render(request, 'store/checkout.html', context)


def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']

     print('Action:', action)
     print('productID:', productId)

     customer = request.user.customer
     product = Product.objects.get(id=productId)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)

     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

     if action == 'add':
          orderItem.quantity = (orderItem.quantity + 1)
     elif action == 'remove':
          orderItem.quantity = (orderItem.quantity - 1)

     orderItem.save()

     if orderItem.quantity <= 0:
          orderItem.delete()

     return JsonResponse('Item was added', safe=False)

#from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt
def processOrder(request):
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          total = float(data['form']['total'])
          order.transaction_id = transaction_id

          if total == float(order.get_cart_total):
               order.complete = True
          order.save()

          if order.shipping == True:
               ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    address=data['shipping']['address'],
                    city=data['shipping']['city'],
                    state=data['shipping']['state'],
                    zipcode=data['shipping']['zipcode'],
                    )
     
     else:
          print('User is not logged in...')
     return JsonResponse('Payment complete!', safe=False)

     def orders(request):
          if request.user.is_authenticated:
               customer = request.user.customer
               order, created = Order.objects.get_or_create(customer=customer, complete=False)
               items = order.orderitem_set.all()
               cartItems = order.get_cart_items
          else:
               items = []
               order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
               cartItems = order['get_cart_items']

          context = {'items':items, 'order':order, 'cartItems':cartItems}
          return render(request, 'store/orders.html', context)

def order_list(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
          items = []
          order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
          cartItems = order['get_cart_items']    
          
     orders = Order.objects.filter(customer = request.user.customer,  complete=True)
     return render(request, 'store/order_list.html', {'orders': orders})

def order_detail(request, pk):
     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
          items = []
          order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}    
          cartItems = order['get_cart_items'] 

     order = Order.objects.get(id=pk)
     order_items = OrderItem.objects.filter(order=order)
     return render(request, 'store/order_detail.html', {'order': order, 'order_items': order_items})