from django.forms import ValidationError
from rest_framework import serializers
from Core.views.serializers.many import ManyChildSerializers
from Core.views.serializers.name import AdaptDataSerializer
from backend.products.app.models import Category, PriceMediator, Product
from rest_framework.fields import empty
from rest_framework.exceptions import ErrorDetail
from backend.providers import Provider



class PriceMediatorForProductSerializer(AdaptDataSerializer, serializers.ModelSerializer):
    # disable require validation because works with ProductSerializer
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)

    def adapt_data(self, data: dict | empty):
        is_empty = data == empty
        data_copy = dict(data) if not is_empty else {}
        if isinstance(data_copy.get('provider'), str):
            provider: Provider | None = Provider.objects.filter(name__iexact=data['provider']).first()
            data_copy['provider'] = provider.id if provider else 0 # 0 is not possible id
        return data_copy if not is_empty else data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['provider'] = instance.provider.name
        del response['product']
        return response

    class Meta:
        model = PriceMediator
        fields = 'id', 'provider', 'price', 'product'


class CategorySerializer(serializers.ModelSerializer):
    # disable unique validation because works with ProductSerializer
    name = serializers.CharField(max_length=200, validators=[])
    
    class Meta:
        model = Category
        fields = 'id', 'name',


class ProductSerializer(serializers.ModelSerializer, ManyChildSerializers):
    providers = PriceMediatorForProductSerializer(many=True)
    category = CategorySerializer()

    def get_or_error_for_category(self, category_data: dict):
        return self.get_or_error(Category.objects.all(), {'name__iexact': category_data.get('name')}, {'category': ['Category not found']})

    def error_or_update_many_for_providers(self, providers_data: list[dict]):
        return self.create_or_update_many(
            providers_data, PriceMediatorForProductSerializer, PriceMediator.objects.all(),
            {'product__id': 'product_id', 'provider__id': 'provider_id'} # product does not repeat provider
        )

    def get_list_many_relationship(self):
        return ['providers']

    def create(self, validated_data):
        # data input
        category_data = validated_data.pop('category')
        providers_data = validated_data.pop('providers')
        providers_data = [{**provider, 'provider': provider['provider'].id} for provider in providers_data]

        # creating for o2o
        category = self.get_or_error_for_category(category_data)
        instance = Product(**validated_data)
        instance.category = category
        instance.save()

        # creating for m2m | creating later because m2m requires product id 
        self.create_many(providers_data, PriceMediatorForProductSerializer, instance.id, 'product')

        return instance

    def update(self, instance, validated_data):
        if self.partial: return self.update_partial(instance, validated_data)
        related_fields_data, validated_data = self.get_data(instance, validated_data)
        self.update_instance(instance, {**validated_data, 'category': self.get_or_error_for_category(related_fields_data['category'])})
        self.error_or_update_many_for_providers(related_fields_data['providers'])
        self.delete_many_instances(instance, self.get_list_many_relationship())
        return instance

    def update_partial(self, instance, validated_data):
        related_fields_data, validated_data = self.get_data(instance, validated_data)

        for attribute_name, value in validated_data.items():
            setattr(instance, attribute_name, value)
        if related_fields_data.get('category') is not None:
            instance.category = self.get_or_error_for_category(related_fields_data['category'])
        instance.save()

        if related_fields_data.get('providers') not in [None, []]:
            self.error_or_update_many_for_providers(related_fields_data['providers'])

        self.delete_many_instances(instance, self.get_list_many_relationship())
        return instance

    def obj_for_get_related_field_data(self) -> dict:
        def get_providers(instance, validated_data):
            providers_data = [{
                'provider_id': provider['provider'], 
                'product_id': instance.id, 'price': provider['price'],
            }  for provider in validated_data]
            return providers_data

        return {
            'category': lambda instance, validated_data : validated_data['category'],
            'providers': get_providers,            
        }

    @property
    def errors(self):
        if not hasattr(self, '_errors'):
            msg = 'You must call `.is_valid()` before accessing `.errors`.'
            raise AssertionError(msg)

        errors = self._errors

        if errors.get('providers'): # list[dict]
            def check_provider_error(provider: dict):
                invalid_error = (provider.get('provider') == [ErrorDetail(string='Invalid pk "0" - object does not exist.', code='does_not_exist')])
                return  provider if not invalid_error else [ErrorDetail(string='Provider not found', code='does_not_exist')]

            new_providers_error = map(check_provider_error, errors['providers'])
            errors['providers'] = list(new_providers_error)
        return errors

    class Meta:
        model = Product
        fields = 'id', 'name', 'description', 'category', 'providers'


