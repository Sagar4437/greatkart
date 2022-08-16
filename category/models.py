from distutils.command.upload import upload
from tabnanny import verbose
from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    # automatic slug creation in category table
    slug = models.SlugField(max_length=100,unique=True)
    desciption = models.TextField(max_length=255, blank=True)
    cat_img = models.ImageField(upload_to='photos/categories/', blank=True)

    # change the plural name of table
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    # string representation of model
    def __str__(self):
        return self.category_name

    # this fun will return the link which is used in menu_links dropdown
    def get_url_for_menu_links(self):
        return reverse('products_by_category', args=[self.slug])