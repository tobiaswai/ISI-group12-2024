from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages

# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']
        shipping_address = request.POST['shipping_address']
        if User.objects.filter(username=username).exists():
            msg = 'This username has already been taken. Please choose a different one.'
            return render(request,'register.html', locals())
        if password != password2:
            msg = 'Passwords are inconsistent'
            return render(request,'register.html',locals())
        #elif username == '' or email == '':
            #msg = 'Please enter required information'
        else:
            User.objects.create_user(username=username, password=password, email=email)
            Customer.objects.create(username=username, password=password, email=email) 
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

