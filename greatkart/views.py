from itertools import product
from django.shortcuts import render

from store.models import Product

def home(request):
    products = Product.objects.all().filter(isAvailable=True)

    return render(request, 'home.html',{'products':products})
