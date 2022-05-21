from venv import create
from rest_framework import serializers
from Core.views.create.many import CreatorForSerializerWithManyFields
from backend.products.app.models import PriceMediator
from backend.providers.app.models import Contact, Provider, Address


class PriceMediatorForProviderSerializer(serializers.ModelSerializer):
    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all(), required=False)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['product'] = instance.product.name
        del response['provider']
        return response

    class Meta:
        model = PriceMediator
        fields = 'id', 'product', 'price', 'provider'


class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = 'id', 'city', 'country'


class ContactSerializer(serializers.ModelSerializer):
    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all(), required=False)
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        del response['provider']
        return response
    
    class Meta:
        model = Contact
        fields = 'id', 'number', 'provider'


class ProviderSerializer(serializers.ModelSerializer, CreatorForSerializerWithManyFields):
    address = AddressSerializer()
    contacts = ContactSerializer(many=True)
    products = PriceMediatorForProviderSerializer(many=True)

    def create(self, validated_data):
        # data input
        address_data = validated_data.pop('address')
        contacts_data = validated_data.pop('contacts')
        products_data = validated_data.pop('products')
        products_data = [{**product, 'product': product['product'].id} for product in products_data]

        # creating for o2o
        address = self.create_instance(address_data, AddressSerializer)
        instance = Provider(**validated_data)
        instance.address = address
        instance.save()

        # creating for m2m | creating later because m2m requires provider id 
        self.create_many(contacts_data, ContactSerializer, instance.id, 'provider')
        self.create_many(products_data, PriceMediatorForProviderSerializer, instance.id, 'provider')

        return instance

    class Meta:
        model = Provider
        fields = 'id', 'name', 'social_role', 'cnpj', 'address', 'contacts', 'products'
