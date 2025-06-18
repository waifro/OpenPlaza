# Create your models here.
import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# crea una cartella sotto l'utente per imagazzinare tutte le foto
def user_directory_path(instance, filename):
    product = instance.product

    # slug per sicurezza e leggibilità
    username = slugify(product.seller.username)
    product_name = slugify(product.name)
    
    # estrai estensione
    ext = filename.split('.')[-1]
    filename = f"{slugify(product.name)}.{ext}"

    # path finale "upload_image/username/productname/filename.png"
    return f'upload_image/{username}/{product_name}/{filename}'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=user_directory_path)