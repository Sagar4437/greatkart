
from tkinter import CASCADE
from django.db import models
from django.urls import reverse

from category.models import Category

# Create your models here.
class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    discription     = models.TextField(max_length=200, blank=True)
    price           = models.IntegerField()
    img             = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    isAvailable     = models.BooleanField(default=True)  

    # on_delete=models.CASCADE will delet all product once we delete category
    # this variable will connect product table and category table
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_details', args=[self.category.slug, self.slug])


class VariationManager(models.Manager):
    def colours(self):
        return super(VariationManager,self).filter(variation_category='colour', is_active=True)

    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size', is_active=True)

variation_category_choice = (
    ('colour','colour'),
    ('size','size') ,
)
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value