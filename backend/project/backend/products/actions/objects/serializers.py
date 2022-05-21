from rest_framework import serializers
from Core.views.create.many import CreatorForSerializerWithManyFields
from backend.products.app.models import Category, PriceMediator, Product



class PriceMediatorForProductSerializer(serializers.ModelSerializer):

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
    
    class Meta:
        model = Category
        fields = 'id', 'name',


class ProductSerializer(serializers.ModelSerializer, CreatorForSerializerWithManyFields):
    providers = PriceMediatorForProductSerializer(many=True)
    category = CategorySerializer()

    def create(self, validated_data):
        # data input
        category_data = validated_data.pop('category')
        providers_data = validated_data.pop('providers')
        providers_data = [{**provider, 'provider': provider['provider'].id} for provider in providers_data]

        # creating for o2o
        category = self.get_or_create_instance(category_data, CategorySerializer, Category.objects.all(), {"name__iexact": category_data.get('name')})
        instance = Product(**validated_data)
        instance.category = category
        instance.save()

        # creating for m2m | creating later because m2m requires product id 
        self.create_many(providers_data, PriceMediatorForProductSerializer, instance.id, 'product')

        return instance

    class Meta:
        model = Product
        fields = 'id', 'name', 'description', 'category', 'providers'


