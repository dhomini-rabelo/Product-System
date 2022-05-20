from rest_framework import serializers
from backend.products.app.models import PriceMediator
from backend.providers.app.models import Contact, Provider, Address


class PriceMediatorForProviderSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['product'] = instance.product.name
        return response

    class Meta:
        model = PriceMediator
        fields = 'id', 'product', 'price'


class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = 'id', 'city', 'country'


class ContactSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Contact
        fields = 'id', 'number',


class ProviderSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    contacts = ContactSerializer(many=True)
    products = PriceMediatorForProviderSerializer(many=True)
    
    class Meta:
        model = Provider
        fields = 'id', 'name', 'social_role', 'cnpj', 'address', 'contacts', 'products'