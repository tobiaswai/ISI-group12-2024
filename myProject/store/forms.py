from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','brand','connectivity_technology','cover_image','description','is_active']
    