from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User (AbstractUser):

    ulubione = models.ManyToManyField('products.Products', related_name = "myproducts" , blank=True)