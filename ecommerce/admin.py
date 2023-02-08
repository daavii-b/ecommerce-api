from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Product


# Apply summernote to all TextField in model.
@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    summernote_fields: str = 'description'

    list_display = ['name', 'stock', 'on_sale', 'price', 'promotional_price']
    list_display_links = ['name']
    list_editable = ['stock', 'on_sale', 'price', 'promotional_price']
    list_per_page = 10
    list_max_show_all = 10

    search_fields = ['name', 'stock', 'on_sale', 'created_at', 'updated_at']
    prepopulated_fields = {
        'slug': ('name',)
    }
