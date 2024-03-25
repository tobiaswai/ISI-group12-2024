from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
import datetime
from django.views import View
from .models import *
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django import forms
from .forms import *
from django.contrib import messages
from django.views.generic import *


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
            auth_login(request, user)
            #msg = 'You have successfully logged in!'
            return redirect('store/main.html')
        else:
            #messages.error(request, 'Invalid credentials.')
            msg = 'username or password is incorrect'
            return render(request,'login.html',locals())
    return render(request, 'login.html')

def adminLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:  # 确保用户是管理员
            auth_login(request, user)
            return redirect('/adminDashboard')
        else:
            error_msg = 'Invalid username or password.'
    return render(request, 'adminLogin.html', locals())

@login_required(login_url="/adminLogin/")
def adminDashboard(request):
     products = Product.objects.all()

     if 'q' in request.GET:
          q = request.GET['q']
          products = Product.objects.filter(Q(name__icontains=q) | Q(id__icontains=q))
     else:
          products = Product.objects.all()

     if request.method == 'POST':
        
        form = ProductForm(request.POST, request.FILES)  # 包含文件数据时需要传入 request.FILES
        if form.is_valid():
          form.save()
          return redirect('/adminDashboard')  # 重定向到更新后的页面或其他视图

        if 'action' in request.POST:
            product_id = request.POST.get('product_id')
            action = request.POST.get('action')

            if action == 'delete':
                # 执行删除产品的操作
                product = Product.objects.get(id=product_id)
                product.delete()
        else:
            # 处理新增产品的操作
            # 这里假设您有一个名为 ProductForm 的表单类用于添加新产品
            form = ProductForm(request.POST)
            if form.is_valid():
                form.save()

     form = ProductForm()

     if request.user.is_staff:
          return render(request, 'adminDashboard.html', {'products': products, 'form': form})
     else:
          return render(request, 'adminLogin.html', locals())

class ProductUpdateView(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        form = ProductForm(instance=product)
        return render(request, 'product_edit.html', {'form': form})

    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/adminDashboard', product_id=product_id)
        
class addImageView(CreateView):
     form_class = ImageForm
     success_url = '/adminDashboard'
     template_name = 'add_images.html'

def Productphotos(request,product_id):
     images= Image.objects.filter(product=product_id)
     context = {'images':images}

     if 'action' in request.POST:
          image = request.POST.get('image_id')
          action = request.POST.get('action')

          if action == 'delete':
               image = Image.objects.get(id=image)
               image.delete()

     return render(request, 'product_images.html', context)


class updateImageView(UpdateView):
     model = Image
     form_class = ImageForm
     success_url = '/adminDashboard'
     template_name = 'update_images.html'


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
     image = Image.objects.filter(product=product)
     context = {'products':product, 'cartItems':cartItems, 'image':image}
     return render(request, 'store/product.html', context)

@login_required
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

def find_related_products(purchased_product):
    return Product.objects.filter(category=purchased_product.category).exclude(id=purchased_product.id)

def generate_recommendations(user):
    purchase_history = Order.objects.filter(customer=user.customer, complete=True)
    recommendations = []
    for order in purchase_history:
        for item in order.orderitem_set.all():
            related_products = find_related_products(item.product)
            recommendations.extend(related_products)
    return recommendations

@login_required
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
     
     recommendations = []
     context = { 'items':items, 'order':order, 'cartItems':cartItems, 'recommendations': recommendations}
     return render(request, 'store/checkout.html', context)

@login_required
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
@login_required
def processOrder(request):
     data = json.loads(request.body)

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          total = float(data['form']['total'])

          if total == float(order.get_cart_total):
               order.complete = True
          order.save()
     
     else:
          print('User is not logged in...')
     return JsonResponse('Payment complete!', safe=False)

@login_required
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

     status = request.GET.get('status')
     if request.user.is_staff:
          if status:
               orders = Order.objects.filter(complete=True,status=status).order_by('-date_ordered')
          else:
               orders = Order.objects.filter(complete=True).order_by('-date_ordered')
     else:
          if status:
               orders = Order.objects.filter(customer = request.user.customer,  complete=True, status=status).order_by('-date_ordered')
          else:
               orders = Order.objects.filter(customer = request.user.customer,  complete=True).order_by('-date_ordered')

     return render(request, 'store/order_list.html', {'orders': orders})

@login_required
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

@login_required
def ship_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user.is_staff and order.status != 'cancelled': 
        order.status = 'shipped'
        order.shipment_date = timezone.now()
        order.save()
    return redirect('order_list')

@login_required
def hold_order(request, order_id):
     order = get_object_or_404(Order, id=order_id)
     if request.user.is_staff and order.status != 'shipped' and order.status != 'cancelled': 
        order.status = 'hold'
        order.save()
     return redirect('order_list')

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user == order.customer.user and order.status != 'shipped':  
        order.status = 'cancelled'
        order.cancel_date = timezone.now()
        order.save()
    return redirect('order_list')
