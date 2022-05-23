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



class ProductDetail(BaseClassForTest):
    
    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.client = Client()
        cls.header = cls.get_header(cls)
        cls.pk = cls.products[0].id
        cls.path = reverse('products:product_detail', kwargs={'pk': cls.pk})
        cls.request = cls.client.get(cls.path, **cls.header)
        cls.valid_data = {
            'name': cls.products[0].name,
            'description': cls.products[0].description,
            'category': {
                "name": cls.products[0].category.name,
            },
            'providers': [
            ]
        }
    
    def test_status(self):
        self.assertEqual(self.request.status_code, 200)

    def test_data(self):
        serializer = ProductSerializer(Product.objects.get(id=self.pk))
        self.assertEqual(
            self.request.data,
            serializer.data
        )
    
    def test_put_method(self):
        data = self.valid_data.copy()
        data['name'] = 'new name'
        request = self.client.put(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['name'], data['name'])

    def test_patch_method(self):
        data = {'name': 'patch name'}
        request = self.client.patch(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['name'], data['name'])

    def test_delete_method(self):
        path = reverse('products:product_detail', kwargs={'pk': self.products[3].id})
        request = self.client.delete(path, **self.header)
        self.assertEqual(request.status_code, 204)

    def test_create_and_change_provider_instance(self):
        provider_name = self.providers[1].name # id != 0
        provider_data = {'provider': provider_name, 'price': '50.00'}
        data = {'providers': [provider_data]}
        request = self.client.patch(self.path, data=data, **self.header)
        self.assertIn(provider_data, [{'provider': provider['provider'], 'price': provider['price']} for provider in request.data['providers']])
        # test change
        new_provider_data = {'provider': provider_name, 'price': '100.00'}
        data = {'providers': [new_provider_data]}
        request = self.client.patch(self.path, data=data, **self.header)
        self.assertIn(new_provider_data, [{'provider': provider['provider'], 'price': provider['price']} for provider in request.data['providers']])

    def test_category_change(self):
        category_name = self.categories[4].name
        request = self.client.patch(self.path, data={'category': {'name': category_name}}, **self.header)
        self.assertEqual(request.data['category'], {'id': request.data['category']['id'], 'name': category_name})

    def test_required_field_error(self):
        request = self.client.put(self.path, data={}, **self.header)
        required_fields = ['name', 'category', 'providers']
        for field_name in required_fields:
            self.assertEqual('This field is required.', str(request.data[field_name][0]))

    def test_category_not_found_error(self):
        request = self.client.patch(self.path, data={'category': {'name': 'not_found_category_name'}}, **self.header)
        self.assertEqual(request.data['category'], ['Category not found'])

    def test_provider_not_found_error(self):
        request = self.client.patch(self.path, data={'providers': [{'provider': 'not_found_name', 'price': '50.00'}]}, **self.header)
        self.assertEqual(str(request.data['providers'][0][0]), 'Provider not found')
