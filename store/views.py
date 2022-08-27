from itertools import product
from logging import exception
from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render


from carts.models import CartItem
from store.models import Product
from category.models import Category
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q

# Create your views here.
def store(request,category_slug=None):
    products = None

    if category_slug != None:
        # get_object_or_404 will fetch category data from DB, If not found return 404
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, isAvailable=True).order_by('id')
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

    else:
        products = Product.objects.all().order_by('id')
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

    return render(request, 'store/store.html',{'products':paged_products})

def product_details(request,category_slug=None,product_slug=None):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        
    except exception as e:
        raise e

    context ={
        'single_product':single_product,
        'in_cart':in_cart,
    }
        
    return render(request, 'store/product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        if keyword:
            products = products = Product.objects.order_by('-created_date').filter(Q(discription__icontains=keyword) | Q(product_name__icontains=keyword))

        context = {
            'products':products,
        }
    return render(request, 'store/store.html',context)