from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','brand','color','image','image2','image3','description','is_active']
    