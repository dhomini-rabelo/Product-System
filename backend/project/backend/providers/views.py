from rest_framework import generics
from Core.support.renders import SimpleRenderer
from Core.views.data_control.create import DataControlAndCreateApi
from backend.providers.actions.objects.serializers import AddressSerializer, ContactSerializer, ProviderSerializer
from backend.providers.app.models import Address, Contact, Provider
from backend.providers.actions.objects.data_control.provider.filter import provider_filter
from backend.providers.actions.objects.data_control.provider.selector import provider_selector



class ProviderListAndCreate(SimpleRenderer, DataControlAndCreateApi):
    serializer_class = ProviderSerializer
    initial_queryset = Provider.objects.all().select_related('address').prefetch_related('contacts', 'products')
    filter_function = provider_filter.filter_queryset
    selector_function = provider_selector.select
    

class ProviderDetail(SimpleRenderer, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all().select_related('address').prefetch_related('contacts', 'products')
