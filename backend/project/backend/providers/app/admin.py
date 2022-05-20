from django.contrib import admin
from backend.providers.app.models import Contact, Provider, Address


admin.site.empty_value_display = 'NULL'




@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',
    list_display_links = 'name',
    list_per_page = 50
    list_select_related = 'address', # use tuple, default is False
    ordering = 'name',
    search_fields = 'name', # ^ -> startswith, = -> iexact, @ ->	search, None -> icontains



@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = 'id', 'number',
    list_display_links = 'number',
    list_per_page = 50
    list_select_related = 'provider', # use tuple, default is False
    ordering = 'number',
    search_fields = 'number', # ^ -> startswith, = -> iexact, @ ->	search, None -> icontains


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = 'id', 'city',
    list_display_links = 'city',
    list_per_page = 50
    ordering = 'city',
    search_fields = 'city', # ^ -> startswith, = -> iexact, @ ->	search, None -> icontains
