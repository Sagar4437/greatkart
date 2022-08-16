from django.contrib import admin
from .models import Product
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name','price','stock','isAvailable','category','modified_date']
    prepopulated_fields = {'slug':('product_name',),'discription':('product_name',)}

admin.site.register(Product,ProductAdmin)
