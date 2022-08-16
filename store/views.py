from logging import exception
from unicodedata import category
from django.shortcuts import get_object_or_404, render
from store.models import Product
from category.models import Category

# Create your views here.
def store(request,category_slug=None):
    products = None

    if category_slug != None:
        # get_object_or_404 will fetch category data from DB, If not found return 404
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, isAvailable=True)

    else:
        products = Product.objects.all()

    return render(request, 'store/store.html',{'products':products})

def product_details(request,category_slug=None,product_slug=None):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except exception as e:
        raise e
        
    return render(request, 'store/product_detail.html',{'single_product':single_product})