from rest_framework import generics
from Core.views.data_control.create import DataControlAndCreateApi
from backend.providers.actions.objects.serializers import AddressSerializer, ContactSerializer, CreateProviderSerializer, ProviderSerializer
from backend.providers.app.models import Address, Contact, Provider
from backend.providers.actions.objects.data_control.provider.filter import provider_filter
from backend.providers.actions.objects.data_control.provider.selector import provider_selector


class ProviderListAndCreate(DataControlAndCreateApi):
    serializer_class = ProviderSerializer
    post_serializer_class = CreateProviderSerializer
    initial_queryset = Provider.objects.all()
    filter_function = provider_filter.filter_queryset
    selector_function = provider_selector.select


class ProviderDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateProviderSerializer
    queryset = Provider.objects.all()


class ContactCreate(generics.CreateAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


class AddressCreate(generics.CreateAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()