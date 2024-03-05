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
    path('order_list/', views.order_list, name="order_list"),
    path('order_detail/<int:pk>', views.order_detail, name="order_detail"),
    path('adminLogin/', views.adminLogin, name="adminLogin"),
    path('adminDashboard/', views.adminDashboard, name="adminDashboard"),
    path('product_edit/<int:product_id>', views.ProductUpdateView.as_view(), name="product_edit"),
    path('order_ship/<int:order_id>/ship/', views.ship_order, name="order_ship"),
    path('order_hold/<int:order_id>/hold/', views.hold_order, name="order_hold"),
    path('order_cancel/<int:order_id>/cancel/', views.cancel_order, name="order_cancel"),
]