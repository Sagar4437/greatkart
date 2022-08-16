from unicodedata import category
from django.contrib import admin
from .models import Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):

    # automatic slug creation in category table
    prepopulated_fields= {"slug":('category_name',), 'desciption':('category_name',)}
    list_display= ['category_name','slug']

admin.site.register(Category,CategoryAdmin)

