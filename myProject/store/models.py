from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'customer', null=True, blank=True, verbose_name=_('user'))
    full_name = models.CharField(max_length=200, null=True, verbose_name=_('full_name'))
    email = models.CharField(max_length=200, null=True, verbose_name=_('email'))
    password = models.CharField(max_length=200, null=True, verbose_name=_('password'))
    shipping_address = models.CharField(max_length=200, null=True, verbose_name=_('shipping_address'))

    def __str__(self):
        return str(self.full_name)

class Product(models.Model):
    name = models.CharField(max_length=200, null=True, verbose_name=_('name'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('price'))
    brand = models.CharField(max_length=16, null=True, verbose_name=_('brand'))
    connectivity_technology = models.CharField(max_length=32, null=True, verbose_name=_('connectivity_technology'))
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, verbose_name=_('description'))
    is_active = models.BooleanField(default=True, verbose_name=_('is_active'))

    def __str__(self):
        return self.name
    
    @property
    def imageURLs(self):
        urls = []
        try:
            if self.image:
                urls.append(self.image.url)
            if self.image2:
                urls.append(self.image2.url)
            if self.image3:
                urls.append(self.image3.url)
        except:
            pass  # handle the exception as needed
        return urls

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('shipped', _('Shipped')),
        ('cancelled', _('Cancelled')),
        ('hold', _('Hold')),]
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('customer'))
    date_ordered = models.DateTimeField(default=timezone.now, verbose_name=_('date_ordered'))
    complete = models.BooleanField(default=False, null=True, blank=False)
    total_amount = models.DecimalField(max_digits=100, decimal_places=2, null=True, verbose_name=_('total_amount'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name=_('status'))
    shipment_date = models.DateTimeField(null=True, blank=True, verbose_name=_('shipment_date'))
    cancel_date = models.DateTimeField(null=True, blank=True, verbose_name=_('cancel_date'))

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def total_amount(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.date_ordered = timezone.now()
        return super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name=_('product'))
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name=_('order'))
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name=_('quantity'))
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_('date_added'))
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name=_('unit_price'))
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name=_('subtotal'))

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    