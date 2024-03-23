from modeltranslation.translator import translator, TranslationOptions
from .models import *

class ProductTranslationOptions(TranslationOptions):
    fields = ("name","description")


translator.register(Product, ProductTranslationOptions)
