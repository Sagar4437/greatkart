import imp
from os import link
from category.models import Category

def menu_list(requst):
    links = Category.objects.all()
    return {'menu_links':links}