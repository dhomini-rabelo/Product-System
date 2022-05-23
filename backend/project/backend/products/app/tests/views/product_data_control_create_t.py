from django.test import TestCase, Client
from unittest import expectedFailure
from random import randint
from django.db.models import Model
from decimal import Decimal
from datetime import date
from django.urls import reverse, resolve
from backend.accounts.app.models import User
from backend.products.actions.objects.serializers import CategorySerializer, ProductSerializer
from backend.products.app.models import Category, PriceMediator, Product
from backend.providers.app.models import Address, Provider
from test.backend.base import BaseClassForTest
from django.db.models import Q



class ProductDataControlAndCreateTest(BaseClassForTest):
    
    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.client = Client()
        cls.header = cls.get_header(cls)
        cls.path = reverse('products:product_list')
        cls.request = cls.client.get(cls.path, **cls.header)
        cls.valid_data = {
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

    def test_status(self):
        self.assertEqual(self.request.status_code, 200)

    def test_data(self):
        serializer = ProductSerializer(Product.objects.all(), many=True)
        self.assertEqual(
            self.request.data,
            serializer.data
        )

    def test_post_method(self):
        request = self.client.post(self.path, data=self.valid_data, **self.header)
        self.assertEqual(request.status_code, 201)

    def test_category_not_found_error(self):
        data = self.valid_data.copy()
        data['category'] = {'name': 'not_found_category_name'}
        request = self.client.post(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual(request.data['category'], ['Category not found'])

    def test_provider_not_found_error(self):
        data = self.valid_data.copy()
        data['providers'] = [{'price': Decimal('1000.50'), 'provider': 'invalid_provider_name'}]
        request = self.client.post(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual(str(request.data['providers'][0][0]), 'Provider not found')

    def test_required_field_error(self):
        request = self.client.post(self.path, data={}, **self.header)
        required_fields = ['name', 'category']
        for field_name in required_fields:
            self.assertEqual('This field is required.', str(request.data[field_name][0]))

    def test_unique_name_error(self):
        data =self.valid_data.copy()
        data = {'name': self.products[9].name}
        request = self.client.post(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual(str(request.data['name'][0]), 'product with this name already exists.')