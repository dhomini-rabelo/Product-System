from django.test import TestCase, Client
from unittest import expectedFailure
from random import randint
from django.db.models import Model
from decimal import Decimal
from datetime import date
from django.urls import reverse
from backend.accounts.app.models import User
from backend.products.actions.objects.serializers import CategorySerializer, ProductSerializer
from backend.products.app.models import Category, PriceMediator, Product
from backend.providers.app.models import Address, Provider
from test.backend.base import BaseClassForTest



class ProductSerializerTest(BaseClassForTest):
    
    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.serializer = ProductSerializer(instance=cls.products[1])
        cls.serializer_many = ProductSerializer(instance=Product.objects.all(), many=True)
        cls.valid_data_1 = {
            'name': 'test',
            'description': 'test',
            'category': {
                "name": cls.categories[0].name,
            },
            'providers': [
                {
                    "provider": cls.providers[0].name,
                    "price": Decimal(f'{randint(1000, 5000)}.00')
                }
            ]
        }
        cls.valid_data_2 = {
            'name': 'test',
            'description': 'test',
            'category': {
                "name": cls.categories[1].name,
            },
            'providers': [
            ]
        }

    def test_default_creation(self):
        test_serializer = ProductSerializer(data=self.valid_data_1)
        test_serializer_2 = ProductSerializer(data=self.valid_data_2)
        self.assertTrue(test_serializer.is_valid())
        self.assertTrue(test_serializer_2.is_valid())

    def test_data_for_serializer(self):
        product = {
            'id': self.products[1].id,
            'name': self.products[1].name,
            'description': self.products[1].description,
            'category': {
                "id": self.products[1].category.id,
                "name": self.products[1].category.name,
            },
            'providers': [{
                    "id": price.id,
                    "provider": price.provider.name,
                    "price": str(price.price)
            } for price in self.products[1].providers.all()]
        }
        data = self.serializer.data.copy()
        data['category'] = dict(data['category'])
        data['providers'] = [dict(product) for product in data['providers']]
        self.assertEqual(self.serializer.data, product)

    def test_error_required_name_field(self):
        serializer = ProductSerializer(data={})
        self.assertFalse(serializer.is_valid())
        required_fields = ['providers', 'category', 'name']
        for field_name in required_fields:
            self.assertEqual('This field is required.', str(serializer.errors[field_name][0]))
    
    def test_unique_name_error(self):
        serializer = ProductSerializer(data={'name': self.products[2].name})
        self.assertFalse(serializer.is_valid())
        self.assertEqual('product with this name already exists.', str(serializer.errors['name'][0]))