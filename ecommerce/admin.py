from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'inventory', 'created_at', 'updated_at']
    list_display_links = ['name']
    list_editable = ['inventory']
    list_per_page = 10
    list_max_show_all = 10

    search_fields = ['name', 'inventory', 'created_at', 'updated_at']
    prepopulated_fields = {
        'slug': ('name',)
    }
