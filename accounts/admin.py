from django.contrib import admin
from .models import Account

from django.contrib.auth.admin import UserAdmin
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'is_active', 'date_joined')

    # when clickedd on link, it will open details
    list_display_links = ('email', 'first_name', 'last_name')

    # readonly fields
    readonly_fields = ('date_joined','last_login')

    # sort users joined_date in desc order
    ordering = ('-date_joined',)

    # mandetory
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account,AccountAdmin)
