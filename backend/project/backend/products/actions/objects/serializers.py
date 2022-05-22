from turtle import update
from types import FunctionType
from rest_framework import serializers
from Core.views.create.many import SerializerSupport
from backend.products.app.models import Category, PriceMediator, Product



class PriceMediatorForProductSerializer(serializers.ModelSerializer):
    # disable require validation because works with ProductSerializer
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['provider'] = instance.provider.name
        del response['product']
        return response

    class Meta:
        model = PriceMediator
        fields = 'id', 'provider', 'price', 'product'


class PriceMediatorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PriceMediator
        fields = 'id', 'provider', 'price', 'product'


class CategorySerializer(serializers.ModelSerializer):
    # disable unique validation because works with ProductSerializer
    name = serializers.CharField(max_length=200, validators=[])
    
    class Meta:
        model = Category
        fields = 'id', 'name',


class ProductSerializer(serializers.ModelSerializer, SerializerSupport):
    providers = PriceMediatorForProductSerializer(many=True)
    category = CategorySerializer()

    def get_or_error_for_category(self, category_data: dict):
        return self.get_or_error(Category.objects.all(), {'name__iexact': category_data.get('name')}, {'category': ['Category not found']})

    def error_or_update_many_for_providers(self, providers_data: list[dict]):
        return self.create_or_update_many(
            providers_data, PriceMediatorForProductSerializer, PriceMediator.objects.all(),
            {'id': 'id', 'product__id': 'product_id'}
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
                'id': provider.get('id'), 'provider_id': provider['provider'], 
                'product_id': instance.id, 'price': provider['price'],
            }  for provider in self.initial_data['providers']]
            return providers_data

        return {
            'category': lambda instance, validated_data : validated_data['category'],
            'providers': get_providers,            
        }

    class Meta:
        model = Product
        fields = 'id', 'name', 'description', 'category', 'providers'


