from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'stock', 'on_sale', 'price', 'promotional_price']
    list_display_links = ['name']
    list_editable = ['stock', 'on_sale', 'price', 'promotional_price']
    list_per_page = 10
    list_max_show_all = 10

    search_fields = ['name', 'stock', 'on_sale', 'created_at', 'updated_at']
    prepopulated_fields = {
        'slug': ('name',)
    }
