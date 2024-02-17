from django.urls import path

from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('product/<int:pk>', views.product , name="product"),
    path('product_list/', views.ProductListView.as_view(), name="product_list"),
]