from types import FunctionType
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

    def error_or_update_instance_for_address(self, address_data: dict, instance):
        return self.error_or_update_instance(
            address_data, Address.objects.all(), {'id': instance.address.id}, {'address': ['Id not found']}
        )

    def create_or_update_many_for_contacts(self, contacts_data: list[dict]):
        return self.create_or_update_many(
            contacts_data, ContactSerializer, Contact.objects.all(),
            {'id': 'id', 'provider__id': 'provider_id'}, 
        )

    def create_or_update_many_for_products(self, products_data: list[dict]):
        return self.create_or_update_many(
            products_data, PriceMediatorForProviderSerializer, 
            PriceMediator.objects.all(), {'id': 'id', 'provider__id': 'provider_id'}
        )

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
        if self.partial: return self.update_partial(instance, validated_data)
        related_fields_data, validated_data = self.get_data(instance, validated_data)
        self.update_instance(instance, {**validated_data, 'address': self.error_or_update_instance_for_address(related_fields_data['address'], instance)})
        self.create_or_update_many_for_contacts(related_fields_data['contacts'])
        self.create_or_update_many_for_products(related_fields_data['products'])
        return instance

    def update_partial(self, instance, validated_data):
        related_fields_data, validated_data = self.get_data(instance, validated_data)

        for attribute_name, value in validated_data.items():
            setattr(instance, attribute_name, value)
        if related_fields_data.get('address') is not None:
            instance.address = self.error_or_update_instance_for_address(related_fields_data['address'], instance)
        instance.save()

        if related_fields_data.get('products') not in [None, []]:
            self.create_or_update_many_for_products(related_fields_data['products'])
        if related_fields_data.get('contacts') not in [None, []]:
            self.create_or_update_many_for_contacts(related_fields_data['contacts'])
        return instance        

    def obj_for_get_related_field_data(self) -> dict:
        def get_contacts(instance, validated_data):
            contacts_data = [{
                'id': contact.get('id'), 'number': contact['number'], 'provider_id': instance.id,
            }  for contact in self.initial_data['contacts']]
            return contacts_data

        def get_products(instance, validated_data):
            products_data = [{
                'id': product.get('id'), 'product_id': product['product'], 'price': product['price'], 'provider_id': instance.id,
            }  for product in self.initial_data['products']]
            return products_data

        return {
            'address': lambda instance, validated_data : validated_data['address'],
            'contacts': get_contacts,            
            'products': get_products,            
        }        

    class Meta:
        model = Provider
        fields = 'id', 'name', 'social_role', 'cnpj', 'address', 'contacts', 'products'
