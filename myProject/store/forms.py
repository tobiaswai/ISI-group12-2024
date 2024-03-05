from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','size','weight','image','description','is_active']
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 4 * 1024 * 1024:  # 限制图像大小为4MB
                raise forms.ValidationError("The image file is too large (max 4MB)")
        return image

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','size','weight','image','image2','image3','description','is_active']