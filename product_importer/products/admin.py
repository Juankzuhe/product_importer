from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["sku", "name", "description"]
    search_fields = ["sku", "name", "description"]
    list_filter = ["is_active"]
