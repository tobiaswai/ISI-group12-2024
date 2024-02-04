from django.urls import path
from accounts.views import *  # the “.” means current directory

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]
