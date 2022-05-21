from venv import create
from rest_framework import serializers
from Core.views.create.many import SerializerSupport
from backend.products.app.models import PriceMediator
from backend.providers.app.models import Contact, Provider, Address


class PriceMediatorForProviderSerializer(serializers.ModelSerializer):
    # disable require validation because works with ProviderSerializer
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
    # disable require validation because works with ProviderSerializer
    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all(), required=False)
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        del response['provider']
        return response
    
    class Meta:
        model = Contact
        fields = 'id', 'number', 'provider'


class ProviderSerializer(serializers.ModelSerializer, SerializerSupport):
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

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        del validated_data['contacts']
        del validated_data['products']
        contacts_data = [{
            'id': contact.get('id'), 'number': contact['number'], 'provider_id': instance.id,
        }  for contact in self.initial_data['contacts']]
        products_data = [{
            'id': product.get('id'), 'product_id': product['product'], 'price': product['price'], 'provider_id': instance.id,
        }  for product in self.initial_data['products']]

        address = self.error_or_update_instance(address_data, Address.objects.all(), {'id': instance.address.id}, {'address': ['Id not found']})
        for attribute_name, value in validated_data.items():
            setattr(instance, attribute_name, value)
        instance.address = address

        instance.save()

        self.error_or_update_many(
            contacts_data, Contact.objects.all(), {'id': 'id', 'provider__id': 'provider_id'},
            {'contacts': ['Id not found or id is none']}
        )

        self.error_or_update_many(
            products_data, PriceMediator.objects.all(), {'id': 'id', 'provider__id': 'provider_id'},
            {'products': ['Id not found or id is none']}
        )

        return instance

    class Meta:
        model = Provider
        fields = 'id', 'name', 'social_role', 'cnpj', 'address', 'contacts', 'products'
