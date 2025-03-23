from typing import Iterable
import stripe 
from django.db import models
from django.conf import settings
from users.models import User
from django.db.models import Sum


stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=128 , unique=True) 
    description = models.TextField(null=True , blank=True)

    def __str__(self):
        return self.name
    
class Brands(models.Model):
    name = models.CharField(max_length=128 , unique=True) 

    def __str__(self):
        return self.name

class  Products(models.Model):

   
    class GenderChoices(models.TextChoices):
        Man = 'Man', 
        Woman = 'Woman', 
        Unisex = 'Unisex',
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    
    image = models.ImageField(upload_to="product_image" , blank=True)
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GenderChoices.choices , default=GenderChoices.Unisex)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    brands = models.ForeignKey(to=Brands, on_delete=models.CASCADE)

    def __str__(self):
        return f'Продукт : {self.name} | Категория: {self.category.name} | Категория: {self.gender}'
    
    def save(self , force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Products, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price * 100), currency='pln')
        return stripe_product_price
    
    def total_sum_quantity(self):
        total = self.product_in_productsize.aggregate(total=Sum('quantity'))['total'] or 0
        return total

class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_image')

    def __str__(self):
        return f"Image for {self.product.name}"


class Size(models.Model):
    size = models.CharField(max_length=10)
    def __str__(self):
        return f"Size {self.size  }"
    

class ProductSize(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product_in_productsize')
    size = models.ForeignKey(Size , on_delete=models.CASCADE, related_name='product_size')
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Product: {self.product.name} | Size: {self.size.size}"


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)
    
    def total_quantity(self):
        return sum(basket.quantity for basket in self )
    
    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete = models.CASCADE)
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    size = models.CharField(max_length=10, blank=True, null=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Продукт : {self.product.name} | Корзина : {self.user.email}'
    
    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'product_image': self.product.image.url,  # Добавлено .url для получения доступного URL изображения
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item
        