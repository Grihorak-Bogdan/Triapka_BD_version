from django.contrib import admin
from products.models import ProductCategory , Products , ProductImage , Brands , ProductSize , Size
# Register your models here.

admin.site.register(Products) ,
admin.site.register(ProductImage) ,
admin.site.register(ProductCategory) ,
admin.site.register(Brands) ,
admin.site.register(ProductSize) ,
admin.site.register(Size) ,