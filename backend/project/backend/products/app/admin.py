from django.contrib import admin
from backend.products.app.models import Category, PriceMediator, Product


admin.site.empty_value_display = 'NULL'




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',
    list_display_links = 'name',
    list_per_page = 50
    list_select_related = 'category', # use tuple, default is False
    ordering = 'name',
    search_fields = 'name', # ^ -> startswith, = -> iexact, @ ->	search, None -> icontains


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',
    list_display_links = 'name',
    list_per_page = 50
    ordering = 'name',
    search_fields = 'name', # ^ -> startswith, = -> iexact, @ ->	search, None -> icontains


@admin.register(PriceMediator)
class PriceMediatorAdmin(admin.ModelAdmin):
    list_display = 'id', 'price',
    list_display_links = 'price',
    list_per_page = 50
    list_select_related = 'provider', 'product'
    ordering = 'price',
    search_fields = 'price',
