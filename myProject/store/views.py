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
        Customer.objects.create(user=user, shipping_address=shipping_address)
        
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
          products = Product.objects.filter(name__icontains=q)
     else:
          products = Product.objects.all()
          
     page = Paginator(products, 6)
     page_list = request.GET.get('page')
     page = page.get_page(page_list)
     products = Product.objects.all()
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


     def get(self, request, subcategory_id):
          subcategory = get_object_or_404(Subcategories, pk=subcategory_id)

          sort_by = request.GET.get("sort", "l2h") 
          if sort_by == "l2h":
               products = subcategory.products.order_by("price")
          elif sort_by == "h2l":
               products = subcategory.products.order_by("-price")

          category_list = Categories.objects.all()
          return render (request, 'products.html',{"subcategory_list" : products, 'category_list': category_list })

class ProductListView(ListView):
     def get_queryset(self):
          filter_val=self.request.GET.get("filter","")
          order_by=self.request.GET.get("orderby","id")
          if filter_val!="":
               products=Product.objects.filter(Q(name__contains=filter_val) | Q(price__contains=filter_val)).order_by(order_by)
          else:
               products=Product.objects.all().order_by(order_by)
          return products

     def get_context_data(self, **kwargs):
          context = super(ProductListView,self).get_context_data(**kwargs)
          context["filter"] = self.request.GET.get("filter","")
          context["orderby"] = self.request.GET.get("orderby","id")
          context["all_table_fields"] = Product._meta.get_fields()
          return context

     


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

          if total == order.get_cart_total:
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