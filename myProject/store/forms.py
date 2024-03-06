from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','size','weight','image','description','is_active']
    def clean_image(self):
        image = self.cleaned_data.get('image')
        return image

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','size','weight','image','image2','image3','description','is_active']