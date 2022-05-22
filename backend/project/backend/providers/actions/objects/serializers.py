from django.forms import ValidationError
from rest_framework import serializers
from Core.views.serializers.many import ManyChildSerializers
from Core.views.serializers.name import AdaptDataSerializer
from Core.views.serializers.validator import ValidatorSerializer
from backend.products.app.models import PriceMediator, Product
from backend.providers.app.models import Contact, Provider, Address
from rest_framework.fields import empty
from rest_framework.exceptions import ErrorDetail
import re


class PriceMediatorForProviderSerializer(AdaptDataSerializer, serializers.ModelSerializer):
    # disable require validation because works with ProviderSerializer and raises error before adapt data
    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all(), required=False)

    def adapt_data(self, data: dict | empty):
        is_empty = data == empty
        data_copy = dict(data) if not is_empty else {}
        if isinstance(data_copy.get('product'), str):
            product: Product | None = Product.objects.filter(name__iexact=data['product']).first()
            data_copy['product'] = product.id if product else 0 # 0 is not possible id
        return data_copy if not is_empty else data
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['product'] = instance.product.name
        del response['provider']
        return response

    class Meta:
        model = PriceMediator
        fields = 'id', 'product', 'price', 'provider'


class AddressSerializer(ValidatorSerializer, serializers.ModelSerializer):

    def validate(self, data):
        return self.use_individual_validation(data)

    def get_individual_validators(self) -> dict:
        def validate_cep(data: dict):
            if not isinstance(data.get('cep'), str): raise ValidationError({'cep': 'Not a valid string'})
            pattern = re.compile(r'^\d{5}-\d{3}$') # simple regex validation for cep XXXXX-XXX
            match = re.fullmatch(pattern, data['cep'])
            if match is None:
                raise ValidationError({'cep': 'Invalid format, use XXXXX-XXX'})

        return {
            'cep': validate_cep,
        }
    
    class Meta:
        model = Address
        fields = 'id', 'cep', 'road', 'complement', 'neighborhood', 'number'


class ContactSerializer(serializers.ModelSerializer):
    # disable require validation because works with ProviderSerializer and raises error before to process
    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all(), required=False)
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        del response['provider']
        return response
    
    class Meta:
        model = Contact
        fields = 'id', 'number', 'provider'


class ProviderSerializer(serializers.ModelSerializer, ManyChildSerializers):
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
            products_data, PriceMediatorForProviderSerializer, PriceMediator.objects.all(),
            {'product__id': 'product_id', 'provider__id': 'provider_id'} # provider does not repeat product
        )

    def get_list_many_relationship(self):
        # for delete m2m relationship fields
        return ['contacts', 'products']

    def validate(self, data):
        return self.use_individual_validation(data)

    def get_individual_validators(self) -> dict:
        def validate_cnpj(data):
            if not isinstance(data.get('cnpj'), str): raise ValidationError({'cnpj': 'Not a valid string'})
            pattern = re.compile(r'^\d{2}.\d{3}.\d{3}/\d{3}.\d{2}$') # simple regex validation for cnpj
            match = re.fullmatch(pattern, data['cnpj'])
            if match is None:
                raise ValidationError({'cnpj': 'Invalid format, use XX.XXX.XXX/XXX-XX'})

        return {
            'cnpj': validate_cnpj
        }

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
        
        self.delete_many_instances(instance, self.get_list_many_relationship())
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

        self.delete_many_instances(instance, self.get_list_many_relationship())
        return instance        

    def obj_for_get_related_field_data(self) -> dict:
        # see ManyChildSerializers.get_data 
        def get_contacts(instance, validated_data):
            contacts_data = [{
                'id': contact.get('id'), 'number': contact['number'], 'provider_id': instance.id,
            }  for contact in self.initial_data['contacts']] # select contact for edit from id 
            return contacts_data

        def get_products(instance, validated_data):
            products_data = [{
                'product_id': product['product'], 'price': product['price'], 'provider_id': instance.id,
            }  for product in validated_data['products']]
            return products_data

        return {
            'address': lambda instance, validated_data : validated_data['address'],
            'contacts': get_contacts,            
            'products': get_products,            
        }        

    @property
    def errors(self):
        if not hasattr(self, '_errors'):
            msg = 'You must call `.is_valid()` before accessing `.errors`.'
            raise AssertionError(msg)

        errors = self._errors

        if errors.get('products'): # list[dict]
            def check_product_error(product: dict):
                invalid_error = (product.get('product') == [ErrorDetail(string='Invalid pk "0" - object does not exist.', code='does_not_exist')])
                return  product if not invalid_error else [ErrorDetail(string='Product not found', code='does_not_exist')]

            new_products_error = map(check_product_error, errors['products'])
            errors['products'] = list(new_products_error)
        return errors

    class Meta:
        model = Provider
        fields = 'id', 'name', 'social_role', 'cnpj', 'address', 'contacts', 'products'
