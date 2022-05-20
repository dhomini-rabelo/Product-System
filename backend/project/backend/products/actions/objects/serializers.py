from rest_framework import serializers
from backend.products.app.models import Category, PriceMediator, Product



class PriceMediatorForProductSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['provider'] = instance.provider.name
        return response

    class Meta:
        model = PriceMediator
        fields = 'id', 'provider', 'price'


class PriceMediatorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PriceMediator
        fields = 'id', 'provider', 'price', 'product'


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = 'id', 'name',


class ProductSerializer(serializers.ModelSerializer):
    providers = PriceMediatorForProductSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = 'id', 'name', 'description', 'category', 'providers'
