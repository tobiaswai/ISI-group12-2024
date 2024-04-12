from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','name_en','name_zh_hant','price','brand','connectivity_technology','cover_image','description','description_en','description_zh_hant','is_active',]


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['product','image']
